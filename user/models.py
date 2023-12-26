from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
from utils.datetime import get_expiry_time


class User(AbstractUser):
    photo_url = models.CharField('用户头像路径', max_length=128, default='')
    is_login = models.BooleanField('登录状态', default=False)
    is_admin = models.BooleanField('是否为管理员', default=False)
    is_author = models.BooleanField('是否为学者', default=False)
    is_authentication = models.BooleanField('是否实名认证', default=False)
    institution = models.CharField('机构', max_length=128, default='')
    photo_url_out = models.CharField('用户头像外部路径', max_length=255, default='https://sa.leonardsaikou.top/avatar/default_avatar.png')
    true_name = models.CharField('真实姓名', max_length=128, default='')
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="custom_user_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="custom_user_set",
        related_query_name="user",
    )

    class Meta:
        db_table = 'Users'

    def __str__(self):
        return self.username


class Author(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=40)
    normalized_name = models.CharField(max_length=40, null=True)
    affiliation = models.TextField(null=True)
    main_affiliation = models.TextField(null=True)
    level = models.TextField(null=True)
    pub_paper_count = models.IntegerField(null=True)
    pub_patent_count = models.IntegerField(null=True)
    citation_count = models.IntegerField(null=True)
    h_index = models.FloatField(null=True)
    # 添加外键关联到User模型
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='author_profile')


class Follow(models.Model):  # 关注信息
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed_authors')
    author_id = models.CharField(max_length=40, default='')
    author_name = models.CharField(max_length=40, default='')

    def __str__(self):
        return f"{self.user.username} follows {self.author_name}"


class Author_User(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    author_id = models.CharField(max_length=40)


class VerificationCode(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=get_expiry_time)

    def __str__(self):
        return self.email
