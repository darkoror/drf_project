from django.urls import reverse

from authentication.models import User
from blog.models import Post, Like

from mixer.backend.django import mixer
from drf_project.tests import BaseAPITest


class TestBlogCategories(BaseAPITest):

    def setUp(self):
        self.user = self.create_and_login()
        self.user.save()
        self.post = mixer.blend(Post, author=self.user)

    def test_list_authors_post(self):
        resp = self.client.get(reverse('author-post:author-posts-list'))
        self.assertEqual(resp.status_code, 200)

    def test_create_author_post(self):
        data = {
            "title": "test_title",
            "content": "test_content"
        }
        resp = self.client.post(reverse('author-post:author-posts-list'), data=data)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(data["title"], resp.data["title"])

    def test_update_author_post(self):
        data = {
            "title": "another_test_title"
        }
        resp = self.client.patch(reverse('author-post:author-posts-detail', args=(self.post.id,)), data=data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data["title"], resp.data["title"])

    def test_retrieve_author_post(self):
        resp = self.client.get(reverse('author-post:author-posts-detail', args=(self.post.id,)))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.post.title, resp.data["title"])

    def test_delete_author_post(self):
        resp = self.client.delete(reverse('author-post:author-posts-detail', args=(self.post.id,)))
        self.assertEqual(resp.status_code, 204)
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())


class TestSFPost(BaseAPITest):

    def setUp(self):
        self.user = self.create_and_login()
        self.user.save()
        self.user2 = mixer.blend(User)
        self.post = mixer.blend(Post, author=self.user)
        self.post2 = mixer.blend(Post, author=self.user2)

    def test_create_like(self):
        resp = self.client.post(reverse('author-post:posts-like-detail', args=(self.post2.id,)))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(Like.objects.filter(author=self.user, post=self.post2).exists())

    def test_create_like_own_post(self):
        resp = self.client.post(reverse('author-post:posts-like-detail', args=(self.post.id,)))
        self.assertEqual(resp.status_code, 403)
        self.assertFalse(Like.objects.filter(author=self.user, post=self.post).exists())
