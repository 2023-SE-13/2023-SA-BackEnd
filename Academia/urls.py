from django.urls import path
from Academia.views import *


urlpatterns = [
    # path('url_name', api_name)
    # 这是一个样例，指定路由名为url_name，对应处理函数为当前app内views.py中的api_name
    path('basicsearch', BasicSearch),
    path('multisearch', MultiSearch),
    path('fuzzysearch', FuzzySearch),
    path('authorsearch', AuthorSearch),
    path('authorfuzzysearch', AuthorFuzzySearch),
    path('get_body', get_body),
    path('store_body', store_body),
    path('get_paper', GetPaperByID),
    path('get_author', GetAuthorByID),
    path('favorite_paper', favorite_paper),
    path('show_favorites', show_favorites),
    path('return_data', ReturnData),
]