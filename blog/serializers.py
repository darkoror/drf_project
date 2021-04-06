from rest_framework import serializers

from blog.models import Post, Like


# class PostLikesSerializer(serializers.ModelSerializer):
#     author = serializers.SlugRelatedField(slug_field="username", read_only=True)
#
#     class Meta:
#         model = Like
#         fields = ("author",)
#
#
# class PostListSerializer(serializers.ModelSerializer):
#     author = serializers.SlugRelatedField(slug_field="username", read_only=True)
#     likes = PostLikesSerializer(many=True)
#
#     class Meta:
#         model = Post
#         fields = '__all__'
#
#
# class PostDetailSerializer(serializers.ModelSerializer):
#     author = serializers.SlugRelatedField(slug_field="username", read_only=True)
#     likes = PostLikesSerializer(many=True)
#
#     class Meta:
#         model = Post
#         fields = '__all__'
#
#
# class PostCreateSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Post
#         fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("title", "content", "created_at", "updated_at", "author")
        read_only_fields = ("created_at", "updated_at", "author")

    def create(self, validated_data):
        author = self.request.user
        instance = super().create(**validated_data)
        instance.author = author
        instance.save()
        return instance

