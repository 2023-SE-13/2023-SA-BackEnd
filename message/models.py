from django.db import models
from django.utils import timezone

from user.models import User


# Create your models here.
class Message(models.Model):
    KINDS = (
        ('author', '认领学者'),
        ('paper', '认领论文'),

    )
    title = models.TextField('标题')
    kind = models.CharField('消息种类', max_length=10, choices=KINDS, default='')
    content = models.TextField('消息内容')
    # send_time = models.DateTimeField('发送时间', default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='接收用户')
    photo = models.CharField('消息图片路径', max_length=128, default='', null=True)
    photo_out = models.CharField('外部消息图片路径', max_length=128, default='', null=True)

class MessageToAdmin(models.Model):
    KINDS = (
        ('author', '认领学者'),
        ('paper', '认领论文'),

    )
    kind = models.CharField('消息种类', max_length=10, choices=KINDS, default='')
    title = models.TextField('标题')
    content = models.TextField('消息内容')
    send_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='发送用户', default='')
    photo = models.CharField('消息图片路径', max_length=128, default='', null=True)
    photo_out = models.CharField('外部消息图片路径', max_length=128, default='', null=True)
