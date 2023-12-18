from django.urls import path
from user.views import *


urlpatterns = [
    # path('url_name', api_name)
    # 这是一个样例，指定路由名为url_name，对应处理函数为当前app内views.py中的api_name
    path('register', register),
    path('login', login),
    path('follow_author', follow_author),
    path('send_code', send_code),

]