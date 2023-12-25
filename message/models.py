from django.db import models
from django.utils import timezone

from user.models import User, Author


# Create your models here.

class ApplyBeAuthor(models.Model):
    title = models.TextField('标题')
    content = models.TextField('消息内容')
    name = models.CharField('姓名', max_length=128,default='')
    send_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='发送用户', default='')
    photo = models.CharField('消息图片路径', max_length=128, default='', null=True)
    photo_out = models.CharField('外部消息图片路径', max_length=128, default='', null=True)
    author_id = models.CharField('学者id',max_length=40)
    created_at = models.DateTimeField('创建时间', auto_now_add=True,null=True)



class ApplyWork(models.Model):
    work_id = models.CharField('成果id', max_length=40)
    send_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='发送用户', default='')
    created_at = models.DateTimeField('创建时间', auto_now_add=True,null=True)



class ReplyToUser(models.Model):
    title = models.TextField('标题')
    content = models.TextField('返回内容')
    receive_user =  models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='接收用户', default='')
