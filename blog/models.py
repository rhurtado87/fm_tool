from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()  
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='like_post', blank=True)

    def __str__(self):
        return self.title

    def like_count(self):
        return self.likes.count()

    def comment_count(self):
        return self.comments.count()

    class Meta:
        ordering = ['-created_at']

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Comment by {self.author.username}'
