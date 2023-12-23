
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
    work_id = request.data.get('work_id')
    work_name = request.data.get('work_name')
    print(work_id)
    print(work_name)

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
        brow_history_list = BrowHistory.objects.filter(user=user)
        ids = [brow_history.id for brow_history in brow_history_list]
        work_names = [brow_history.work_name for brow_history in brow_history_list]
        work_ids = [brow_history.work_id for brow_history in brow_history_list]
        times = [localtime(brow_history.time) for brow_history in brow_history_list]
        response_data = {
            'status': 'success',
            'id': ids,
            'work_name': work_names,
            'work_id': work_ids,
            'time': times,
            'result': 0,
        }
    except BrowHistory.DoesNotExist:
        response_data = {
            'status': 'error',
            'message': 'No BrowHistory found for the given user_id.'
        }

    return JsonResponse(response_data)

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_brow_history(request):
    id = request.data.get("id")
    try:
        user = request.user
        deleted_count = BrowHistory.objects.filter(user=user,id=id).delete()

        if deleted_count == 0:
            raise Exception('删除失败')

        return JsonResponse({'result': 0, 'message': 'BrowHistory deleted successfully'})

    except User.DoesNotExist:
        return JsonResponse({'message': '用户不存在'}, status=400)

    except Exception as e:
        return JsonResponse({'message': str(e)}, status=400)

@api_view(['DELETE'])
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