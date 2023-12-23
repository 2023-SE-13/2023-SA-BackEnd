from django.urls import path

from Administrator.views import *
from Browhistory.views import *

urlpatterns = [
    # path('url_name', api_name)
    # 这是一个样例，指定路由名为url_name，对应处理函数为当前app内views.py中的api_name
    path('add_brow_history', add_brow_history),
    path('get_work_list', get_work_list),
    path('delete_brow_history', delete_brow_history),
    path('delete_all_brow_history', delete_all_brow_history)
]