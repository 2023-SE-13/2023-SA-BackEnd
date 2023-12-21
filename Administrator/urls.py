from django.urls import path

from Administrator.views import *

urlpatterns = [
    # path('url_name', api_name)
    # 这是一个样例，指定路由名为url_name，对应处理函数为当前app内views.py中的api_name
    path('show_author_message', show_author_message),
    path('show_paper_message', show_paper_message),
    path('handle_author_message', handle_author_message),
    path('handle_paper_message', handle_paper_message),
    path('get_specific_author_apply', get_specific_author_apply),

]