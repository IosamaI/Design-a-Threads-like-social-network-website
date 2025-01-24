from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class User(AbstractUser):
    pass


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    text = models.CharField(max_length=1000, null=True, default=None, blank=True)
    date_time = models.DateTimeField(auto_now_add=True, blank=True)
    likes = models.ManyToManyField(User, related_name="likes", blank=True)

    def __str__(self):
        return f"{self.user}'s post | Post ID: {self.id}"


class Follow_data(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follow_data")
    followers = models.ManyToManyField(User, related_name="followers", blank=True)
    follows = models.ManyToManyField(User, related_name="follows", blank=True)

    def __str__(self):
        return f"{self.user}'s follow data"
