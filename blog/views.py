from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, status, filters

from blog.models import Post, Like
from blog.serializers import PostSerializer, SFPostSerializer, CreateLikeSerializer


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
        # serializer = self.get_serializer(data=self.request.data, context={"post": self.get_object(),
        #                                                                   "user": self.request.user})
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        post = self.get_object()
        user = self.request.user
        if post.author == user:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        like, created = Like.objects.get_or_create(post=post, author=user)
        if not created:
            like.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    # @action(detail=True, methods=['DELETE'], permission_classes=(IsAuthenticated,))
    # def delete_like(self, request, *args, **kwargs):
    #     post = self.get_object()
    #     user = self.request.user
    #     try:
    #         like = Like.objects.get(post=post, author=user)
    #     except Like.DoesNotExist:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)
    #
    #     like.delete()
    #
    #     return Response(status=status.HTTP_204_NO_CONTENT)


