from django.db import models
from user.models import User
# Create your models here.

class BrowHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,to_field='id')
    time = models.DateTimeField(auto_now_add=True)
    work_id = models.CharField('work_id', max_length=255)
    work_name = models.CharField('work_name', max_length=255)

