from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, status, filters

from blog.models import Post, Like
from blog.serializers import PostSerializer, SFPostSerializer


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
    """
    serializer_class = PostSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

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

    like:
    Create or destroy like for post

    Create or destroy one like for post
    """
    permission_classes = (AllowAny,)
    serializer_class = SFPostSerializer
    queryset = Post.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    @action(detail=True, methods=['POST'], permission_classes=(IsAuthenticated,))
    def like(self, request, *args, **kwargs):
        obj = self.get_object()
        user = self.request.user
        like = Like.objects.filter(post=obj, author=user)
        if like:
            like.delete()
        else:
            if obj.author == user:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            Like.objects.create(post=obj, author=user)
        return Response(status=status.HTTP_200_OK)
