from rest_framework.routers import SimpleRouter

from blog import views

app_name = 'author-post'
author_post_router = SimpleRouter()
author_post_router.register('author/posts', views.AuthorPost, basename='author-posts')
author_post_router.register('posts', views.SFAuthorPost, basename='sf-posts')

urlpatterns = []

urlpatterns += author_post_router.urls
