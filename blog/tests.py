from django.urls import reverse
from rest_framework import status

from authentication.models import User
from blog.models import Post, Like

from mixer.backend.django import mixer
from drf_project.tests import BaseAPITest


class TestBlogCategories(BaseAPITest):  # author

    def setUp(self):
        self.user = self.create_and_login()
        self.post = mixer.blend(Post, author=self.user)
        self.user2 = mixer.blend(User)
        self.post2 = mixer.blend(Post, author=self.user2)
        self.data = {
            "title": "test_title",
            "content": "test_content"
        }

    def test_author_list_posts(self):
        resp = self.client.get(reverse('author-post:author-posts-list'))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_author_not_authorized_list_posts(self):
        self.logout()
        resp = self.client.get(reverse('author-post:author-posts-list'))
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_author_create_post(self):
        resp = self.client.post(reverse('author-post:author-posts-list'), data=self.data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.data["title"], resp.data["title"])
        self.assertEqual(Post.objects.get(id=resp.data["id"]).author, self.user)

    def test_author_create_post_not_authorized(self):
        self.logout()
        resp = self.client.post(reverse('author-post:author-posts-list'), data=self.data)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_author_create_post_no_data(self):
        self.data["title"] = ""
        self.data["content"] = ""
        resp = self.client.post(reverse('author-post:author-posts-list'), data=self.data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_author_update_post(self):
        self.data.pop("content")
        resp = self.client.patch(reverse('author-post:author-posts-detail', args=(self.post.id,)), data=self.data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(self.data["title"], resp.data["title"])
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, self.data["title"])

    def test_author_update_not_own_post(self):
        title = self.post.title
        self.logout()
        self.user = self.create_and_login(username="qq", email="qqqqqq@gmail.com")
        resp = self.client.patch(reverse('author-post:author-posts-detail', args=(self.post.id,)), data=self.data)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, title)

    def test_author_update_post_not_authorized(self):
        self.logout()
        self.data.pop("content")
        resp = self.client.patch(reverse('author-post:author-posts-detail', args=(self.post.id,)), data=self.data)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_author_retrieve_post(self):
        resp = self.client.get(reverse('author-post:author-posts-detail', args=(self.post.id,)))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(self.post.title, resp.data["title"])

    def test_author_not_authorized_retrieve_post(self):
        self.logout()
        resp = self.client.get(reverse('author-post:author-posts-detail', args=(self.post.id,)))
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_author_retrieve_post_deleted(self):
        self.client.delete(reverse('author-post:author-posts-detail', args=(self.post.id,)))
        resp = self.client.get(reverse('author-post:author-posts-detail', args=(self.post.id,)))
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())

    def test_author_delete_post(self):
        resp = self.client.delete(reverse('author-post:author-posts-detail', args=(self.post.id,)))
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())

    def test_delete_not_own_post(self):
        resp = self.client.delete(reverse('author-post:author-posts-detail', args=(self.post2.id,)))
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Post.objects.filter(id=self.post2.id).exists())

    def test_delete_post_deleted(self):
        self.client.delete(reverse('author-post:author-posts-detail', args=(self.post.id,)))
        resp = self.client.delete(reverse('author-post:author-posts-detail', args=(self.post.id,)))
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())


class TestPost(BaseAPITest):

    def setUp(self):
        self.user = self.create_and_login()
        self.user2 = mixer.blend(User)
        self.post = mixer.blend(Post, author=self.user)
        self.post2 = mixer.blend(Post, author=self.user2)

    def test_list_posts(self):
        resp = self.client.get(reverse('author-post:posts-list'))
        self.assertEqual(resp.status_code, 200)

    def test_create_like(self):
        resp = self.client.post(reverse('author-post:posts-like', args=(self.post2.id,)))
        self.assertEqual(resp.status_code, 204)
        self.assertTrue(Like.objects.filter(author=self.user, post=self.post2).exists())

    def test_remove_like(self):
        self.client.post(reverse('author-post:posts-like', args=(self.post2.id,)))
        resp2 = self.client.post(reverse('author-post:posts-like', args=(self.post2.id,)))
        self.assertEqual(resp2.status_code, 204)
        self.assertFalse(Like.objects.filter(author=self.user, post=self.post2).exists())

    def test_create_like_own_post(self):
        resp = self.client.post(reverse('author-post:posts-like', args=(self.post.id,)))
        self.assertEqual(resp.status_code, 400)
        self.assertFalse(Like.objects.filter(author=self.user, post=self.post).exists())


class TestSearchPost(BaseAPITest):
    def setUp(self):
        self.user = self.create()
        self.post1 = Post.objects.create(title="some post", content="some post", author=self.user)
        self.post2 = Post.objects.create(title="some article", content="some article", author=self.user)

    def test_search_post1(self):
        resp = self.client.get(f"{reverse('author-post:posts-list')}?search=post")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data[0]["title"], self.post1.title)

    def test_search_post2(self):
        resp = self.client.get(f"{reverse('author-post:posts-list')}?search=article")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data[0]["title"], self.post2.title)

    def test_search_post_find_no_post(self):
        resp = self.client.get(f"{reverse('author-post:posts-list')}?search=qqq")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 0)

    def test_search_post_both(self):
        resp = self.client.get(f"{reverse('author-post:posts-list')}?search=some")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 2)
