from django.db import models
from django.utils import timezone

from user.models import User


# Create your models here.
class Message(models.Model):
    title = models.TextField('标题')
    content = models.TextField('消息内容')
    # send_time = models.DateTimeField('发送时间', default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='接收用户')


class MessageToAdmin(models.Model):
    title = models.TextField('标题')
    content = models.TextField('消息内容')

