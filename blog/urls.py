from rest_framework.routers import SimpleRouter

from blog import views

app_name = 'author-post'
author_post_router = SimpleRouter(trailing_slash=False)
author_post_router.register('posts/author', views.AuthorPostView, basename='author-posts')
author_post_router.register('posts', views.PostView, basename='posts')

urlpatterns = []

urlpatterns += author_post_router.urls
