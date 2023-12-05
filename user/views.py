from django.http import JsonResponse
from django.shortcuts import render

from user.models import User


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

