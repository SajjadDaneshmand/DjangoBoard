from django.contrib.auth.models import User
from django.utils.text import Truncator
from django.db import models

# Create your models here.


class Board(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.name

    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()

    def get_last_post(self):
        return Post.objects.filter(topic__board=self).last()


class Topic(models.Model):
    subject = models.CharField(max_length=255)
    last_update = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board, related_name='topics', null=True, on_delete=models.SET_NULL)
    starter = models.ForeignKey(User, related_name='topics', null=True, on_delete=models.SET_NULL)
    views = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return self.subject


class Post(models.Model):
    message = models.TextField(max_length=5000)
    topic = models.ForeignKey(Topic, related_name='posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)

    def __str__(self):
        truncated_message = Truncator(self.message)
        return truncated_message.chars(30)
