from django.db import models

from user.models import User


class Work_Data(models.Model):
    browse_times = models.IntegerField(default=0)
    work_id = models.CharField('work_id', max_length=40)
    title = models.CharField('title', max_length=255)


class Work_Author(models.Model):
    author_id = models.CharField('author_id', max_length=40)
    work_id = models.CharField('work_id', max_length=40)


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article_name = models.CharField(max_length=255)
    article_id = models.CharField(max_length=40)


class Body_User(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Body = models.TextField()
