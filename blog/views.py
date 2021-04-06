from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, viewsets
from django_filters.rest_framework import DjangoFilterBackend

from blog.models import Post
from blog.serializers import PostSerializer
from blog.service import PostFilter

#
# class PostListView(generics.ListAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostListSerializer
#     filter_backends = (DjangoFilterBackend,)
#     filterset_class = PostFilter
#
#
# class PostDetailView(APIView):
#     def get(self, request, pk):
#         post = Post.objects.get(id=pk)
#         serializer = PostDetailSerializer(post)
#         return Response(serializer.data)


# class PostCreateView(APIView):
#     def post(self, request):
#         blog_post = PostCreateSerializer(data=request.data)
#         if blog_post.is_valid():
#             blog_post.save()
#         return Response(status=201)


class AuthorPost(viewsets.ModelViewSet):
    serializer_class = PostSerializer

    def get_queryset(self, *args, **kwargs):
        return Post.objects.filter(author=self.request.user)


class SFAuthorPost(viewsets.ReadOnlyModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
