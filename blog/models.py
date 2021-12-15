from django.db import models
from authentication.models import User


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='posts_images', null=True, blank=True, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'posts'
        verbose_name = "Post"
        verbose_name_plural = "Posts"


class Like(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="author_likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, related_name="post_likes")

    def __str__(self):
        return f"{self.author}, {self.post}"

    class Meta:
        db_table = 'likes'
        verbose_name = "Like"
        verbose_name_plural = "Likes"
        unique_together = ("author", "post")
