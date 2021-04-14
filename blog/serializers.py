from rest_framework import serializers, status
from rest_framework.response import Response

from blog.models import Post, Like


class PostSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    author = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Post
        fields = ("id", "title", "content", "created_at", "updated_at", "author", "likes")
        read_only_fields = ("id", "created_at", "updated_at", "author")

    def get_likes(self, obj):
        return obj.likes.count()


class SFPostSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = ("id", "title", "content", "created_at", "updated_at", "author", "likes")
        read_only_fields = ("id", "created_at", "updated_at", "author")

    def get_likes(self, obj):
        return obj.likes.count()


class CreateLikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ("id",)

    def validate_duplicate(self, user, post):
        like = Like.objects.filter(post=post, author=user)
        if like:
            raise serializers.ValidationError("You have already liked the post")

    def validate_like_own_post(self, user, post):
        if post.author == user:
            raise serializers.ValidationError("You cant like your own post")

    def validate(self, data):
        user = self.context["user"]
        post = self.context["post"]
        self.validate_duplicate(user, post)
        self.validate_like_own_post(user, post)

        return data

    def create(self, validated_data):
        validated_data["author"] = self.context["user"]
        validated_data["post"] = self.context["post"]
        like = super().create(validated_data)
        return like
