from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated

from message.models import MessageToAdmin
from user.models import User


# Create your views here.

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def show_all_message(request):
    if request.method == 'GET':
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        if user.is_admin:
            messages = MessageToAdmin.objects.all()
            messages_list = [{
                'id':  message.id,
                'kind': message.kind,
                'send_user': message.send_user.username,  # 假设你想返回发送用户的用户名
            } for message in messages]
            result = {'result': 0, 'messages': messages_list}
            return JsonResponse(result)
        else:
            result = {'result': 1, 'messages': "无权限查看"}
            return JsonResponse(result)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def show_author_message(request):
    if request.method == 'GET':
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        if user.is_admin:
            messages = MessageToAdmin.objects.filter(kind="author")
            messages_list = [{
                'id':  message.id,
                'kind': message.kind,
                'send_user': message.send_user.username,  # 假设你想返回发送用户的用户名
            } for message in messages]
            result = {'result': 0, 'messages': messages_list}
            return JsonResponse(result)
        else:
            result = {'result': 1, 'messages': "无权限查看"}
            return JsonResponse(result)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def show_paper_message(request):
    if request.method == 'GET':
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        if user.is_admin:
            messages = MessageToAdmin.objects.filter(kind="paper")
            messages_list = [{
                'id':  message.id,
                'kind': message.kind,
                'send_user': message.send_user.username,  # 假设你想返回发送用户的用户名
            } for message in messages]
            result = {'result': 0, 'messages': messages_list}
            return JsonResponse(result)
        else:
            result = {'result': 1, 'messages': "无权限查看"}
            return JsonResponse(result)

