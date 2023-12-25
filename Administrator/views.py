from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from django.utils.dateformat import DateFormat
from Academia.models import Work_Author
from message.models import ApplyBeAuthor, ApplyWork, ReplyToUser
from user.models import User, Author_User


# Create your views here.


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def show_author_message(request):
    if request.method == 'GET':
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        if user.is_admin:
            messages = ApplyBeAuthor.objects.all()
            messages_list = [{
                'id': message.id,
                'author_id': message.author_id,
                'username': message.send_user.username,  # 假设你想返回发送用户的用户名
                'send_user_id': message.send_user.id,
                'datetime': DateFormat(message.created_at).format('Y-m-d H:i')
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
            messages = ApplyWork.objects.all()
            messages_list = [{
                'id': message.id,
                'work_id': message.work_id,
                'send_user': message.send_user.username,  # 假设你想返回发送用户的用户名
                'send_user_id': message.send_user.id,
                'author_id': Author_User.objects.get(user=message.send_user)
            } for message in messages]
            result = {'result': 0, 'messages': messages_list}
            return JsonResponse(result)
        else:
            result = {'result': 1, 'messages': "无权限查看"}
            return JsonResponse(result)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def handle_author_message(request):
    if request.method == 'POST':
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        result = request.POST.get('result')
        message_id = request.POST.get('message_id')
        message = ApplyBeAuthor.objects.get(id=message_id)

        if user.is_admin:
            if result == "0":
                reply = ReplyToUser.objects.create(
                    receive_user=message.send_user,
                    title="认领学者处理结果",
                    content="处理号：" + str(message.id) + "很遗憾，您的认证失败，请完善信息后重试",
                )
                message.delete()
            if result == "1":
                reply = ReplyToUser.objects.create(
                    receive_user=message.send_user,
                    title="认领学者处理结果",
                    content="处理号：" + str(message.id) + "您的认证成功",
                )
                message.send_user.is_author=True
                message.send_user.save()
                Author_User.objects.create(
                    user=message.send_user,
                    author_id=message.author_id,
                )
                ApplyBeAuthor.objects.filter(send_user=message.send_user).delete()
            result = {'result': 0, 'message': "处理成功"}
            return JsonResponse(result)
        else:
            result = {'result': 1, 'messages': "无权限查看"}
            return JsonResponse(result)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def handle_paper_message(request):
    if request.method == 'POST':
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        result = request.POST.get('result')
        message_id = request.POST.get('message_id')
        message = ApplyWork.objects.get(id=message_id)

        if user.is_admin:
            if result == "0":
                reply = ReplyToUser.objects.create(
                    receive_user=message.send_user,
                    title="认领成果处理结果",
                    content="处理号：" + str(message.id) + "很遗憾，您的认证失败，请完善信息后重试",
                )
                message.delete()
            if result == "1":
                reply = ReplyToUser.objects.create(
                    receive_user=message.send_user,
                    title="认领成果处理结果",
                    content="处理号：" + str(message.id) + "您的认领成功，该成果已在您名下并更新",
                )
                Work_Author.objects.create(
                    author_id=Author_User.objects.get(user=message.send_user).author_id,
                    work_id=message.work_id,
                )
                ApplyWork.objects.filter(send_user=message.send_user).delete()
            result = {'result': 0, 'message': "处理成功"}
            return JsonResponse(result)
        else:
            result = {'result': 1, 'messages': "无权限查看"}
            return JsonResponse(result)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_specific_author_apply(request):
    if request.method == 'POST':
        message_id = request.POST.get('message_id')
        user = request.user
        if user.is_admin:
            message = ApplyBeAuthor.objects.get(id=message_id)
            message = {
                'title': message.title,
                'author_id': message.author_id,
                'true_name': message.name,
                'content': message.content,
                'photo_url':message.photo,
                'photo_url_out':message.photo_out,
                'username': message.send_user.username,

            }
            result = {'result': 0, 'message': message}
            return JsonResponse(result)
        else:
            result = {'result': 1, 'messages': "无权限查看"}
            return JsonResponse(result)