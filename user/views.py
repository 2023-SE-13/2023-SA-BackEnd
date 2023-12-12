from django.http import JsonResponse
from django.shortcuts import render

from user.models import User, Follow, Author


# Create your views here.
def register(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    if User.objects.filter(username=username).exists():
        result = {'result': 1, 'message': r'用户名已存在'}
        return JsonResponse(result)

    email = request.POST.get('email', '')
    user = User.objects.create(username=username, password=password, email=email)
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
    if user.password == password:
        request.session['username'] = username
        user = User.objects.get(username=username)
        user.is_login = True
        user.save()
        result = {'result': 0, 'message': r'登录成功'}
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