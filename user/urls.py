from django.urls import path
from user.views import *

urlpatterns = [
    # path('url_name', api_name)
    # 这是一个样例，指定路由名为url_name，对应处理函数为当前app内views.py中的api_name
    path('register', register),
    path('login', login),
    path('follow_author', follow_author),
    path('send_code', send_code),
    path('verify_code', verify_code),
    path('apply_author', apply_author),
    path('apply_admin', apply_admin),
    path('apply_work', apply_work),
    path('get_apply_results', get_apply_results),
    path('show_follow_author', show_follow_author),
    path('upload_avatar', upload_avatar),
    path('change_user_name', change_user_name),
    path('change_user_email', change_user_email),
    path('change_user_password', change_user_password),
    path('authentication', authentication),
]
