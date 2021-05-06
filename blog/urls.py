from rest_framework.routers import SimpleRouter

from blog import views

app_name = 'author-post'

author_post_router = SimpleRouter()
author_post_router.register('posts/author', views.AuthorPostView, basename='author-posts')
author_post_router.register('posts', views.PostView, basename='posts')

urlpatterns = [] + author_post_router.urls
