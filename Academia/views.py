# Create your views here.
from django.http import JsonResponse
from elasticsearch.client import Elasticsearch
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from models import *
from .models import Favorite
from .serializers import *

es = Elasticsearch(hosts='elastic:yXC0ZTAbjmhmyLHb7fBv@116.63.49.180:9200')


def BasicSearch(request):
    search_data = json.loads(request.body.decode('utf-8'))
    # page = search_data.get('page')
    # size = 20
    search_content = search_data.get('search_content')
    search_field = search_data.get('search_field')
    sort_by = search_data.get('sort_by')
    sort_order = search_data.get('sort_order')
    includes = ["title",
                "publication_date",
                "authorships.author.display_name"]
    if sort_by != "":
        body = {
            "query": {
                "match": {
                    search_field: search_content
                }
            },
            # "from": (page - 1) * size,
            # "size": size,
            "sort": [
                {
                    sort_by: {
                        "order": sort_order
                    }
                }
            ],
            "_source": {
                "includes": includes
            },

        }
    else:
        body = {
            "query": {
                "match": {
                    search_field: search_content
                }
            },
            # "from": (page - 1) * size,
            # "size": size,
            "_source": {
                "includes": includes
            },

        }
    # print(body)
    res = es.search(index="works", body=body)
    res = res['hits']
    return JsonResponse(res, safe=False)


def MultiSearch(request):
    search_data = json.loads(request.body.decode('utf-8'))
    sort_by = search_data.get('sort_by')
    sort_order = search_data.get('sort_order')
    search_list = search_data.get('search_list')
    includes = ["title",
                "publication_date",
                "authorships.author.display_name"]
    # print(search_list)
    match_list = []
    for search_pair in search_list:
        search_content = search_pair['search_content']
        search_field = search_pair['search_field']
        match_object = {
            "match": {
                search_field: search_content
            }
        }
        match_list.append(match_object)
    if sort_by != "":
        body = {
            "query": {
                "bool": {
                    "must": match_list

                }
            },
            "sort": [
                {
                    sort_by: {
                        "order": sort_order
                    }
                }
            ],
            "_source": {
                "includes": includes
            }
        }
    else:
        body = {
            "query": {
                "bool": {
                    "must": match_list

                }
            },
            "_source": {
                "includes": includes
            }
        }
    # print(body)
    res = es.search(index="works", body=body)
    res = res['hits']
    return JsonResponse(res, safe=False)


def FuzzySearch(request):
    search_data = json.loads(request.body.decode('utf-8'))
    # print(search_list)

    search_content = search_data.get('search_content')
    search_field = search_data.get('search_field')
    sort_by = search_data.get('sort_by')
    sort_order = search_data.get('sort_order')
    includes = ["title",
                "publication_date",
                "authorships.author.display_name"]
    if sort_by != "":
        body = {
            "query": {
                "fuzzy": {
                    search_field: search_content
                }
            },
            "sort": [
                {
                    sort_by: {
                        "order": sort_order
                    }
                }
            ],
            "_source": {
                "includes": includes
            }
        }
    else:
        body = {
            "query": {
                "fuzzy": {
                    search_field: search_content
                }
            },
            "_source": {
                "includes": includes
            }
        }
    # print(body)
    res = es.search(index="works", body=body)
    res = res['hits']
    return JsonResponse(res, safe=False)


def AuthorSearch(request):
    search_data = json.loads(request.body.decode('utf-8'))
    # page = search_data.get('page')
    # size = 20
    search_content = search_data.get('search_content')
    search_field = search_data.get('search_field')
    sort_by = search_data.get('sort_by')
    sort_order = search_data.get('sort_order')
    includes = ["display_name",
                "cited_by_count",
                "last_known_institution.display_name"]
    if sort_by != "":
        body = {
            "query": {
                "match": {
                    search_field: search_content
                }
            },
            # "from": (page - 1) * size,
            # "size": size,
            "sort": [
                {
                    sort_by: {
                        "order": sort_order
                    }
                }
            ],
            "_source": {
                "includes": includes
            },

        }
    else:
        body = {
            "query": {
                "match": {
                    search_field: search_content
                }
            },
            # "from": (page - 1) * size,
            # "size": size,
            "_source": {
                "includes": includes
            },

        }
    # print(body)
    res = es.search(index="authors", body=body)
    res = res['hits']
    return JsonResponse(res, safe=False)


def GetPaperByID(request):
    paper_id = request.GET.get('paper_id')

    body = {
        "query": {
            "term": {
                "_id": paper_id
            }
        }
    }
    res = es.search(index="works", body=body)['hits']['hits'][0]
    title = res.get('_source').get('title')
    if Work_Data.objects.filter(work_id=paper_id).exists():
        work_data = Work_Data.objects.get(work_id=paper_id)
        work_data.browse_times += 1
        work_data.save()
    else:
        Work_Data.objects.create(work_id=paper_id, title=title, browse_times=1)
    return JsonResponse(res, safe=False)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def favorite_paper(request):
    if request.method == 'POST':
        # 获取被关注的学者的ID
        paper_id = request.POST.get('paper_id')
        paper_name = request.POST.get('paper_name')

        # 检查用户是否已经收藏了该文章
        if Favorite.objects.filter(user=request.user, article_id = paper_id).exists():
            result = {'result': 1, 'message': r'您已经收藏了该文章'}
            return JsonResponse(result)

        # 创建关注关系

        Favorite.objects.create(user=request.user,article_id=paper_id,article_name=paper_name)
        result = {'result': 0, 'message': r'收藏成功'}
        return JsonResponse(result)
    else:
        result = {'result': 1, 'message': r'无效的请求'}
        return JsonResponse(result)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def show_favorites(request):
    if request.method == 'GET':
            messages = Favorite.objects.filter(user=request.user)
            messages_list = [{
                'paper_id': message.article_id,
                'paper_name': message.article_name,
            } for message in messages]
            result = {'result': 0, 'messages': messages_list}
            return JsonResponse(result)