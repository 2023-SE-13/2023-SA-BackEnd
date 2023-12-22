
from django.utils.timezone import localtime

from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import JsonResponse

from Browhistory.models import BrowHistory
from user.models import User

# Create your views here.
@api_view(['POST'])
def add_brow_history(request):
    user_id = request.data.get('user_id')
    work_id = request.data.get('work_id')
    work_name = request.data.get('work_name')

    # 检查user_id和book_id是否存在
    if not user_id or not work_id or not work_name:
        return JsonResponse({'error': 'user_id and book_id are required.'}, status=400)

    # 获取对应的User对象
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Invalid user_id.'}, status=400)

    # 创建BrowHistory对象并保存到数据库
    brow_history = BrowHistory(user=user, work_id=work_id, work_name=work_name)
    brow_history.save()

    return JsonResponse({'success': 'BrowHistory created.'}, status=201)

@api_view(['GET'])
def get_work_list(request):
    user_id = request.data.get('user_id')
    user = User.objects.get(id=user_id)
    try:
        brow_history_list = BrowHistory.objects.filter(user=user)
        work_names = [brow_history.work_name for brow_history in brow_history_list]
        work_ids = [brow_history.work_id for brow_history in brow_history_list]
        times = [localtime(brow_history.time) for brow_history in brow_history_list]
        response_data = {
            'status': 'success',
            'work_name': work_names,
            'work_id': work_ids,
            'time': times
        }
    except BrowHistory.DoesNotExist:
        response_data = {
            'status': 'error',
            'message': 'No BrowHistory found for the given user_id.'
        }

    return JsonResponse(response_data)

@api_view(['DELETE'])
def delete_brow_history(request):
    user_id = request.data.get('user_id')
    work_id = request.data.get('work_id')
    try:
        user = User.objects.get(id=user_id)
        deleted_count = BrowHistory.objects.filter(user=user, work_id=work_id).delete()

        if deleted_count == 0:
            raise Exception('删除失败')

        return JsonResponse({'message': 'BrowHistory deleted successfully'})

    except User.DoesNotExist:
        return JsonResponse({'message': '用户不存在'}, status=400)

    except Exception as e:
        return JsonResponse({'message': str(e)}, status=400)