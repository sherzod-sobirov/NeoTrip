from django.db import models
from user.models import User
from ckeditor.fields import RichTextField  # Import RichTextField from ckeditor.fields


# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=100)
    body = RichTextField()  # Use RichTextField for the rich text content
    created_at = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to='post_images/')
    tags = models.CharField(max_length=100, blank=True, null=True)

    @property
    def comment_count(self):
        count = self.comment.all().count()
        return count

    def __str__(self) -> str:
        return f"{self.title}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comment")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user}"