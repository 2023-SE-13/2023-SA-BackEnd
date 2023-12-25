from django.http import JsonResponse
from django.db.models import Sum
from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

from Academia.models import Work_Data
from user.models import User, Author_User


# Create your views here.

@api_view(['GET'])
def show_hot(request):
    if request.method == 'GET':
        works = Work_Data.objects.all().order_by('-browse_times')

        # 创建一个列表来保存每条记录的相关信息
        works_list = [{
            'work_id': work.work_id,
            'title': work.title,
            'browse_times': work.browse_times
        } for work in works]

        # 准备返回的结果
        result = {'result': 0, 'works': works_list}
        return JsonResponse(result)


@api_view(['GET'])
def show_all(request):
    if request.method == 'GET':
        user_count = User.objects.count()
        author_user_count = Author_User.objects.count()
        work_data_browse_times_sum = Work_Data.objects.aggregate(total_browse_times=Sum('browse_times'))[
            'total_browse_times']
        work_data_browse_times_sum = work_data_browse_times_sum or 0

        # 创建一个列表来保存每条记录的相关信息
        result = {'result': 0,
                  'user_count' : user_count,
                  'author_count':author_user_count,
                  'browse_times_sum':work_data_browse_times_sum,
                  }

        # 准备返回的结果
        return JsonResponse(result)