from django.urls import path

from message.views import *

urlpatterns = [
    # path('url_name', api_name)
    # 这是一个样例，指定路由名为url_name，对应处理函数为当前app内views.py中的api_name
    path('show_hot', show_hot),
    path('show_all', show_all),

]