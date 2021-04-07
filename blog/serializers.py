from rest_framework import serializers

from blog.models import Post, Like


class PostLikesSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = Like
        fields = ("author",)


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field="username", read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = ("id", "title", "content", "created_at", "updated_at", "author", "likes")
        read_only_fields = ("id", "created_at", "updated_at", "author")

    def create(self, validated_data):
        author = self.context["request"].user
        instance = super().create(validated_data)
        instance.author = author
        instance.save()

        return instance

    def get_likes(self, obj):
        return obj.likes.count()
