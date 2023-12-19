from django.contrib.auth.hashers import check_password, make_password
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.authtoken.models import Token

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
    user = User.objects.get(username=username)

    if check_password(password, user.password):
        token, created = Token.objects.get_or_create(user=user)
        request.session['username'] = username
        user = User.objects.get(username=username)
        user.is_login = True
        user.save()
        result = {'result': 0, 'message': r'登录成功', "token": str(token.key)}
        return JsonResponse(result)
    else:
        result = {'result': 1, 'message': r'用户名或密码错误'}
        return JsonResponse(result)


def follow_author(request):
    if request.method == 'POST':
        # 获取被关注的学者的ID
        author_id = request.POST.get('author_id')
        user_id = request.POST.get('user_id')

        try:
            author = Author.objects.get(id=author_id)
            user = User.objects.get(id=user_id)
        except Author.DoesNotExist:
            result = {'result': 1, 'message': r'学者不存在'}
            return JsonResponse(result)

        # 检查用户是否已经关注了该学者
        if Follow.objects.filter(user=user, author=author).exists():
            result = {'result': 1, 'message': r'您已经关注了该学者'}
            return JsonResponse(result)

        # 创建关注关系
        follow = Follow(user=user, author=author)
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
        #return JsonResponse(result)
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

