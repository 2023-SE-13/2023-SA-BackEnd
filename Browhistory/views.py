
from django.utils.timezone import localtime

from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated

from Browhistory.models import BrowHistory
from user.models import User

# Create your views here.
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_brow_history(request):
    # work_id = request.POST.get('work_id')
    # work_name = request.POST.get('work_name')
    work_id = request.data.get('work_id')
    work_name = request.data.get('work_name')
    # print(work_id)
    # print(work_name)

    # 检查user_id和book_id是否存在
    if not work_id:
        return JsonResponse({'error': 'work_id are required.'}, status=400)
    if not work_name:
        return JsonResponse({'error': 'work_name are required.'}, status=400)

    # 获取对应的User对象
    try:
        user = request.user
    except User.DoesNotExist:
        return JsonResponse({'error': 'Invalid user_id.'}, status=400)

    # 创建BrowHistory对象并保存到数据库
    brow_history = BrowHistory(user=user, work_id=work_id, work_name=work_name)
    brow_history.save()

    return JsonResponse({'result': 0, 'success': 'BrowHistory created.'}, status=201)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_work_list(request):
    user = request.user
    try:
        # 查询当前用户的浏览历史记录
        brow_history_list = BrowHistory.objects.filter(user=user)

        # 构建objects数组，每个浏览历史对象都转换为字典
        objects = [{
            'id': brow_history.id,
            'work_name': brow_history.work_name,
            'work_id': brow_history.work_id,
            'time': localtime(brow_history.time).strftime('%Y-%m-%d %H:%M:%S')  # 格式化时间
        } for brow_history in brow_history_list]

        # 将构建的objects列表附加到响应数据中
        response_data = {
            'status': 'success',
            'objects': objects,
            'result': 0,
        }

    except BrowHistory.DoesNotExist:
        # 如果没有找到BrowHistory，则返回错误状态和信息
        response_data = {
            'status': 'error',
            'message': 'No BrowHistory found for the given user_id.'
        }

    # 返回JSON响应
    return JsonResponse(response_data)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_brow_history(request):
    history_id = request.data.get("id")
    try:
        user = request.user
        deleted_count = BrowHistory.objects.filter(user=user,id=history_id).delete()

        if deleted_count == 0:
            raise Exception('删除失败')

        return JsonResponse({'result': 0, 'message': 'BrowHistory deleted successfully'})

    except User.DoesNotExist:
        return JsonResponse({'message': '用户不存在'}, status=400)

    except Exception as e:
        return JsonResponse({'message': str(e)}, status=400)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_all_brow_history(request):
    try:
        user = request.user
        deleted_count = BrowHistory.objects.filter(user=user).delete()

        if deleted_count == 0:
            raise Exception('删除失败')

        return JsonResponse({'result': 0, 'message': 'BrowHistory all deleted successfully'})

    except User.DoesNotExist:
        return JsonResponse({'message': '用户不存在'}, status=400)

    except Exception as e:
        return JsonResponse({'message': str(e)}, status=400)