import os

from django.contrib.auth.hashers import check_password, make_password
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated

from SA_backend.settings import BASE_DIR
from message.models import ApplyBeAuthor, ApplyWork, ReplyToUser
from user.models import User, Follow, Author
from utils.utils import send_email


# Create your views here.
def register(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    if User.objects.filter(username=username).exists():
        result = {'result': 1, 'message': r'用户名已存在'}
        return JsonResponse(result)

    email = request.POST.get('email', '')
    hashed_password = make_password(password)
    user = User.objects.create(username=username, password=hashed_password, email=email)
    user.save()
    result = {'result': 0, 'message': r'注册成功'}
    return JsonResponse(result)


def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    if not User.objects.filter(username=username):
        result = {'result': 1, 'message': r'用户名或密码错误'}
        return JsonResponse(result)

    try:
        user = User.objects.get(username=username)
        if check_password(password, user.password):
            token, created = Token.objects.get_or_create(user=user)
            return JsonResponse({'result': 0, 'message': r'登录成功', "token": str(token.key)})
        else:
            return JsonResponse({'result': 1, 'message': r'用户名或密码错误'})
    except User.DoesNotExist:
        return JsonResponse({'result': 1, 'message': r'用户名或密码错误'})

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def follow_author(request):
    if request.method == 'POST':
        # 获取被关注的学者的ID
        author_id = request.POST.get('author_id')
        user_id = request.user.id
        author_name = request.POST.get('user_id')


        # 检查用户是否已经关注了该学者
        if Follow.objects.filter(user=request.user, author_id=author_id).exists():
            result = {'result': 1, 'message': r'您已经关注了该学者'}
            return JsonResponse(result)

        # 创建关注关系
        follow = Follow(user=request.user, author_id=author_id,author_name=author_name)
        follow.save()

        result = {'result': 0, 'message': r'关注成功'}
        return JsonResponse(result)
    else:
        result = {'result': 1, 'message': r'无效的请求'}
        return JsonResponse(result)


username_verify = ['' for i in range(100)]
email_verify = ['' for i in range(100)]
code_list = [0 for i in range(100)]


def send_code(request):
    username = request.POST.get('username')
    email = request.POST.get('email')
    user_id = User.objects.get(username=username).id
    if User.objects.filter(username=username, email=email).exists():
        user_id = User.objects.get(username=username).id
        # result = {'result': 0, 'report': r'确认成功'}
        global username_verify
        username_verify[user_id] = username
        global email_verify
        email_verify[user_id] = email
    else:
        result = {'result': 1, 'report': r'邮箱错误'}
        return JsonResponse(result)
    try:
        global code_list
        code_list[user_id] = send_email(email_verify[user_id])
        result = {'result': 0, 'report': r'发送成功'}
        return JsonResponse(result)
        # return JsonResponse(result)
    except:
        result = {'result': 1, 'report': r'发送失败'}
        return JsonResponse(result)


def verify_code(request):
    global code_list
    username = request.POST.get('username')
    user_id = User.objects.get(username=username).id
    code_to_verify = request.POST.get('code')
    print('name:', username, 'code:', code_list[user_id], 'code_to_verify:', code_to_verify)
    if code_list[user_id] == code_to_verify:
        result = {'result': 0, 'report': '验证码正确'}
        return JsonResponse(result)
    else:
        result = {'result': 1, 'report': '验证码错误'}
        return JsonResponse(result)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def apply_author(request):
    if request.method == 'POST':
        author_id = request.POST.get('author_id', '')
        name = request.POST.get('name', '')
        content = request.POST.get('content', '')
        photo = request.FILES.get('photo')

        try:
            message = ApplyBeAuthor.objects.create(

                title="学者申请",
                name=name,
                content=content,
                send_user=request.user,
                author_id=author_id,
                # send_user=user,
            )
            if photo:
                _, ext = os.path.splitext(photo.name)
                avatar_path = os.path.join(BASE_DIR, 'messageToAdmin_photo', f'{message.id}_message.png')

                # 保存头像文件到指定路径
                with open(avatar_path, 'wb') as file:
                    for chunk in photo.chunks():
                        file.write(chunk)

                # 更新用户的头像路径
                message.photo = avatar_path
                message.photo_out = 'http://116.63.49.180:8080/messagetoAdmin/' + f'{message.id}_message.png'
                message.save()
                result = {'result': 0, 'report': r'成功提交申请'}
                return JsonResponse(result)
            else:
                result = {'result': 0, 'report': r'成功提交申请'}
                return JsonResponse(result)
        except ValidationError as e:
            result = {'result': 1, 'report': r'提交申请失败'}
            return JsonResponse(result)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def apply_admin(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        if code == "123456" or code == "567890":
            request.user.is_admin = True
            request.user.save()
            result = {'result': 0, 'report': r'成为管理员'}
            return JsonResponse(result)
        else:
            result = {'result': 1, 'report': r'认证失败'}
            return JsonResponse(result)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def apply_work(request):
    if request.method == 'POST':
        work_id= request.POST.get('work_id', '')
        if request.user.is_author:
                message = ApplyWork.objects.create(

                    send_user=request.user,
                    work_id=work_id,
                    # send_user=user,
                )
                result = {'result': 0, 'report': r'成功提交申请'}
                return JsonResponse(result)
        else:
                result = {'result': 1, 'report': r'不是学者，没有申请资格'}
                return JsonResponse(result)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_apply_results(request):
    if request.method == 'GET':
            messages = ReplyToUser.objects.filter(receive_user=request.user)
            messages_list = [{
                'title': message.title,
                'content': message.content,
            } for message in messages]
            result = {'result': 0, 'messages': messages_list}
            return JsonResponse(result)
