from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField('用户名', max_length=16)
    password = models.CharField('密码', max_length=20)
    email = models.EmailField('邮箱')
    # role = models.CharField('职位', max_length=10, choices=ROLES)
    # created_at = models.DateTimeField('创建日期', auto_now_add=True)
    photo_url = models.CharField('用户头像路径', max_length=128, default='')
    # photo_url_out = models.CharField('外部用户头像路径', max_length=128, default='http://82.157.165.72:8888/photo/default.jpg')
    is_login = models.BooleanField('登录状态', default=False)

    def __str__(self):
        return self.username
# Create your models here.
