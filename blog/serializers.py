from rest_framework import serializers

from blog import constants
from blog.models import Post


class PostSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    author = serializers.CharField(default=serializers.CurrentUserDefault())

    default_error_messages = {
        'access_denied': constants.ACCESS_DENIED_ERROR,
    }

    class Meta:
        model = Post
        fields = ("id", "title", "content", "created_at", "updated_at", "author", "likes", "image")
        read_only_fields = ("id", "created_at", "updated_at", "author")

    def get_likes(self, obj):
        return obj.post_likes.count()

    def validate_change_own_post(self, user, post):
        if user.id != post.author.id:
            self.fail('access_denied')

    def update(self, instance, validated_data):
        self.validate_change_own_post(self.context["request"].user, instance)
        return super().update(instance, validated_data)

    def __delete__(self, instance):
        self.validate_change_own_post(self.context["request"].user, instance)
        # super().__delete__(instance)
        self.__delete__(instance)
