from django.urls import path
from rest_framework.routers import SimpleRouter

from blog import views

app_name = 'author-post'
author_post_router = SimpleRouter()
author_post_router.register('post', views.AuthorPost, basename='author-posts')

urlpatterns = [
    path('posts', views.SFAuthorPost)
] + author_post_router.urls
