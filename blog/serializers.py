from rest_framework import serializers

from blog.models import Post


class AuthorPostSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    author = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Post
        fields = ("id", "title", "content", "created_at", "updated_at", "author", "likes")
        read_only_fields = ("id", "created_at", "updated_at", "author")

    def get_likes(self, obj):
        return obj.post_likes.count()


class PostSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = ("id", "title", "content", "created_at", "updated_at", "author", "likes")
        read_only_fields = ("id", "created_at", "updated_at", "author")

    def get_likes(self, obj):
        return obj.post_likes.count()
