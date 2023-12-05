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
    is_admin = models.BooleanField('是否为管理员',default=False)

    def __str__(self):
        return self.username


class Author(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=40)
    normalized_name = models.CharField(max_length=40)
    affiliation = models.TextField()
    main_affiliation = models.TextField()
    level = models.TextField()
    pub_paper_count = models.IntegerField()
    pub_patent_count = models.IntegerField()
    citation_count = models.IntegerField()
    h_index = models.FloatField()
    # 添加外键关联到User模型
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='author_profile')
