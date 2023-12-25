from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

from Academia.models import Work_Data


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