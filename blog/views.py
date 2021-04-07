from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, viewsets, mixins, status
from django_filters.rest_framework import DjangoFilterBackend

from blog.models import Post, Like
from blog.serializers import PostSerializer
from blog.service import PostFilter


class AuthorPost(viewsets.ModelViewSet):
    """
    retrieve:
    Get a author post

    Get one author post

    list:
    Get list of author posts

    Get full list of author posts

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

    like:
    Create or destroy like for post

    Create or destroy one like for post
    """
    serializer_class = PostSerializer

    def get_queryset(self, *args, **kwargs):
        return Post.objects.filter(author=self.request.user)


class SFAuthorPost(viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    Get a post

    Get one post

    list:
    Get list of posts

    Get full list of posts
    """
    permission_classes = (AllowAny,)
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PostFilter

    @action(detail=True, methods=['POST'], permission_classes=(IsAuthenticated,))
    def like(self, request, ref=None):
        obj = self.get_object()
        user = self.request.user
        like = Like.objects.filter(post=obj, author=user)
        if like:
            like.delete()
        else:
            if obj.author == user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            Like.objects.create(post=obj, author=user)
        return Response(status=status.HTTP_200_OK)
