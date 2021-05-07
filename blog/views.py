from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import viewsets, status, filters

from blog.models import Post, Like
from blog.serializers import PostSerializer


class PostView(viewsets.ModelViewSet):
    """
    retrieve:
    Get a post

    Get one post

    list:
    Get list of posts

    Get full list of posts

    create:
    Create new author post

    Create one author post

    update:
    Update new author post

    Update one author post

    destroy:
    Delete author post

    Delete one author post

    partial_update:
    Update some author post

    Partial update one author post
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    def destroy(self, request, *args, **kwargs):
        post = self.get_object()
        if request.user.id == post.author.id:
            return super(PostView, self).destroy(self, request, *args, **kwargs)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['POST'], permission_classes=(IsAuthenticated,))
    def like(self, request, *args, **kwargs):
        post = self.get_object()
        user = self.request.user
        if post.author == user:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        like, created = Like.objects.get_or_create(post=post, author=user)
        if not created:
            like.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
