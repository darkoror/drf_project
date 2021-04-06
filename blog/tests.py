from django.urls import reverse

from blog.models import Post

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
