import os
import random

from django.contrib.auth.hashers import check_password, make_password
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

from SA_backend.settings import BASE_DIR
from message.models import ApplyBeAuthor, ApplyWork, ReplyToUser
from user.models import User, Follow, Author, VerificationCode, Author_User
from utils.utils import send_email


# Create your views here.
def register(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    code = request.POST.get('code', '')
    email = request.POST.get('email', '')
    if not password or not email or not code or not username:
        return JsonResponse({'result': 1, 'message': r'缺少必要信息'})

    verification_code = VerificationCode.objects.filter(email=email).order_by('-created_at').first()

    if not verification_code or verification_code.code != code:
        return JsonResponse({'result': 1, 'message': r'验证码错误'})

    if verification_code.expires_at < timezone.now():
        print(verification_code.expires_at)
        print(timezone.now())
        return JsonResponse({'result': 1, 'message': r'验证码已过期'})

    if User.objects.filter(username=username).exists():
        result = {'result': 1, 'message': r'用户名已存在'}
        return JsonResponse(result)

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
            return JsonResponse({'result': 0, 'message': r'登录成功', "token": str(token.key), 'is_admin': user.is_admin})
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
        author_name = request.POST.get('author_name')

        # 检查用户是否已经关注了该学者
        if Follow.objects.filter(user=request.user, author_id=author_id).exists():
            result = {'result': 1, 'message': r'您已经关注了该学者'}
            return JsonResponse(result)

        # 创建关注关系
        follow = Follow(user=request.user, author_id=author_id, author_name=author_name)
        follow.save()

        result = {'result': 0, 'message': r'关注成功'}
        return JsonResponse(result)
    else:
        result = {'result': 1, 'message': r'无效的请求'}
        return JsonResponse(result)


username_verify = ['' for i in range(100)]
email_verify = ['' for i in range(100)]
code_list = [0 for i in range(100)]


@api_view(['POST'])
def send_code(request):
    email = request.POST.get('email')
    code = str(random.randint(1000, 9999))
    VerificationCode.objects.create(email=email, code=code)
    send_email(email, code)
    return JsonResponse({'result': 0, 'message': r'验证码已发送'})


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
                avatar_path = os.path.join(BASE_DIR, 'messagetoAdmin', f'{message.id}_message.png')

                # 保存头像文件到指定路径
                with open(avatar_path, 'wb') as file:
                    for chunk in photo.chunks():
                        file.write(chunk)

                # 更新用户的头像路径
                message.photo = avatar_path
                message.photo_out = 'http://116.63.49.180/messagetoAdmin/' + f'{message.id}_message.png'
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
        work_id = request.POST.get('work_id', '')
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


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def show_follow_author(request):
    if request.method == 'GET':
        messages = Follow.objects.filter(user=request.user)
        messages_list = [{
            'author_id': message.author_id,
            'author_name': message.author_name,
        } for message in messages]
        result = {'result': 0, 'messages': messages_list}
        return JsonResponse(result)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def upload_avatar(request):
    user = request.user
    avatar = request.FILES.get('avatar')

    if avatar:  # 如果上传了头像文件
        # 生成头像文件的保存路径
        _, ext = os.path.splitext(avatar.name)
        avatar_path = os.path.join(BASE_DIR, 'avatar', f'{user.id}_avatar.png')

        # 保存头像文件到指定路径
        with open(avatar_path, 'wb') as file:
            for chunk in avatar.chunks():
                file.write(chunk)

        # 更新用户的头像路径
        user.photo_url = avatar_path
        user.photo_url_out = 'http://116.63.49.180/avatar/' + f'{user.id}_avatar.png'
        user.save()
        result = {'result': 0, 'report': r'上传成功'}
        return JsonResponse(result)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def change_user_name(request):
    if request.method == 'POST':
        user = request.user
        new_name = request.data.get('username')

        try:
            user.username = new_name
            user.save()
            return JsonResponse({'result': 0, 'message': 'User name updated successfully.'})
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found.'}, status=404)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def change_user_email(request):
    if request.method == 'POST':
        user = request.user
        new_email = request.data.get('email')

        try:
            # print(user.email)
            # print(new_email)
            user.email = new_email
            user.save()
            return JsonResponse({'result': 0, 'message': 'User email updated successfully.'})
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found.'}, status=404)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def change_user_password(request):
    if request.method == 'POST':
        user = request.user
        new_password = request.data.get('password')

        try:
            # print(user.email)
            # print(new_email)
            user.set_password(new_password)
            user.save()
            print(new_password)
            print(user.password)
            return JsonResponse({'result': 0, 'new_password':
                new_password,
                                 'user_changed_password':user.password})
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found.'}, status=404)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_self_information(request):
    if request.method == 'GET':
        user = request.user
        try:
            response_data = {
                'id': user.id,
                'username': user.username,
                'last_login': user.last_login,
                'is_superuser': user.is_superuser,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'is_staff': user.is_staff,
                'is_active': user.is_active,
                'date_joined': user.date_joined,
                'photo_url': user.photo_url,
                'is_login': user.is_login,
                'is_admin': user.is_admin,
                'is_author': user.is_author,
                'result': 0,
                'photo_url_out': user.photo_url_out,
                'author_id': "",
                'is_authentication':user.is_authentication,
                'true_name':user.true_name,
            }
            author_user = Author_User.objects.filter(user=user).first()
            if author_user:
                response_data['author_id'] = author_user.author_id
            return JsonResponse(response_data)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found.'}, status=404)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def authentication(request):
    if request.method == 'POST':
        user = request.user
        true_name = request.POST.get('true_name')
        ID = request.POST.get('ID')
        institution = request.POST.get('institution')
        request.user.true_name = true_name
        # request.user.ID = ID
        request.user.institution = institution
        request.user.is_authentication = True
        request.user.save()
        return JsonResponse({'result': 0, 'message': '认证成功'})


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_specific_information(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = User.objects.get(id=user_id)

        try:
            response_data = {
                'id': user.id,
                'username': user.username,
                'last_login': user.last_login,
                'is_superuser': user.is_superuser,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'is_staff': user.is_staff,
                'is_active': user.is_active,
                'date_joined': user.date_joined,
                'photo_url': user.photo_url,
                'is_login': user.is_login,
                'is_admin': user.is_admin,
                'is_author': user.is_author,
                'result': 0,
                'photo_url_out': user.photo_url_out,
                'author_id': "",
                'is_authentication': user.is_authentication,
                'true_name': user.true_name,
            }
            author_user = Author_User.objects.filter(user=user).first()
            if author_user:
                response_data['author_id'] = author_user.author_id
            return JsonResponse(response_data)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found.'}, status=404)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)
