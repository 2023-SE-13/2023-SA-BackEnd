# Create your views here.
import json
import string

from django.http import JsonResponse
from elasticsearch.client import Elasticsearch
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from elasticsearch import helpers
from .models import *
from user.models import Author_User

es = Elasticsearch(hosts='elastic:yXC0ZTAbjmhmyLHb7fBv@116.63.49.180:9200', timeout=30, max_retries=10,
                   retry_on_timeout=True)
sample_abstract_inverted_index = {
    "Despite": [
        0
    ],
    "growing": [
        1
    ],
    "interest": [
        2
    ],
    "in": [
        3,
        4,
        6,
    ],
    "Open": [
        5,
        7
    ]
}


def reconstruct_text(inverted_index):
    words = list(inverted_index.keys())  # 获取所有单词
    max_position = max(max(positions) for positions in inverted_index.values())  # 获取最大位置值

    # 初始化一个位置列表，用于构建文本
    text_positions = [None] * (max_position + 1)

    # 遍历反向索引
    for word, positions in inverted_index.items():
        for position in positions:
            text_positions[position] = word  # 将单词放置到对应的位置

    # 根据位置列表构建原始文本
    reconstructed_txt = ' '.join(text_positions)
    return reconstructed_txt


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
                "authorships.author.display_name",
                "keywords.keyword",
                "abstract_inverted_index",
                "primary_location.source.display_name",
                "language",
                "concepts.display_name"]
    if sort_by != "":
        if "." in search_field:
            field_left = ""
            field_right = ""
            index = search_field.find('.')  # 找到第一个.的位置
            if index != -1:
                field_left = search_field[:index]  # 获取最后一个.之前的部分
                field_right = search_field[index + 1:]  # 获取最后一个.之后的部
            body = {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "nested": {
                                    "path": field_left,
                                    "query": {

                                        "match": {
                                            search_field: search_content
                                        }

                                    }
                                }
                            }
                        ]
                    }
                },
                "sort": [
                    {
                        sort_by: {
                            "order": sort_order
                        }
                    }
                ],
                # "from": (page - 1) * size,
                # "size": size,
                "_source": {
                    "includes": includes
                },
                "highlight": {
                    "fields": {
                        search_field: {}
                    },
                    "pre_tags": "<font color='red'>",
                    "post_tags": "</font>",
                },
                "track_total_hits": 1000
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
                "highlight": {
                    "fields": {
                        search_field: {}
                    },
                    "pre_tags": "<font color='red'>",
                    "post_tags": "</font>",
                },
                "track_total_hits": 1000
            }
    else:
        if "." in search_field:
            field_left = ""
            field_right = ""
            index = search_field.find('.')  # 找到第一个.的位置
            if index != -1:
                field_left = search_field[:index]  # 获取最后一个.之前的部分
                field_right = search_field[index + 1:]  # 获取最后一个.之后的部
            body = {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "nested": {
                                    "path": field_left,
                                    "query": {

                                        "match": {
                                            search_field: search_content
                                        }

                                    }
                                }
                            }
                        ]
                    }
                },
                # "from": (page - 1) * size,
                # "size": size,
                "_source": {
                    "includes": includes
                },
                "highlight": {
                    "fields": {
                        search_field: {}
                    },
                    "pre_tags": "<font color='red'>",
                    "post_tags": "</font>",
                },
                "track_total_hits": 1000
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
                "highlight": {
                    "fields": {
                        search_field: {}
                    },
                    "pre_tags": "<font color='red'>",
                    "post_tags": "</font>",
                },
                "track_total_hits": 1000
            }
    print(body)
    res = es.search(index="works", body=body, size=1000)
    res = res['hits']
    return JsonResponse(res, safe=False)


def MultiSearch(request):
    search_data = json.loads(request.body.decode('utf-8'))
    sort_by = search_data.get('sort_by')
    sort_order = search_data.get('sort_order')
    search_list = search_data.get('search_list')
    includes = ["title",
                "publication_date",
                "authorships.author.display_name",
                "keywords.keyword",
                "abstract_inverted_index",
                "primary_location.source.display_name",
                "language",
                "concepts.display_name"]
    # print(search_list)
    match_list = []
    highlighy_list = []
    for search_pair in search_list:
        search_content = search_pair['search_content']
        search_field = search_pair['search_field']
        if search_field == "authorships.author.display_name":
            match_object = {
                "nested": {
                    "path": "authorships",
                    "query": {
                        "match": {
                            search_field: search_content
                        }
                    }
                }
            }
        elif search_field == "keywords.keyword":
            match_object = {
                "nested": {
                    "path": "keywords",
                    "query": {
                        "match": {
                            search_field: search_content
                        }
                    }
                }
            }
        else:
            match_object = {
                "match": {
                    search_field: search_content
                }
            }

        highlighy_object = {
            search_field: {}
        }
        match_list.append(match_object)
        highlighy_list.append(highlighy_object)
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
            },
            "highlight": {
                "fields": highlighy_list,
                "pre_tags": "<font color='red'>",
                "post_tags": "</font>",
            },
            "track_total_hits": 1000

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
            },
            "highlight": {
                "fields": highlighy_list,
                "pre_tags": "<font color='red'>",
                "post_tags": "</font>",
            },
            "track_total_hits": 1000

        }
    # print(body)
    res = es.search(index="works", body=body, size=1000)
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
                "authorships.author.display_name",
                "keywords.keyword",
                "abstract_inverted_index",
                "primary_location.source.display_name",
                "language",
                "concepts.display_name"]
    if sort_by != "":
        if "." in search_field:
            field_left = ""
            field_right = ""
            index = search_field.find('.')
            if index != -1:
                field_left = search_field[:index]
                field_right = search_field[index + 1:]

            body = {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "nested": {
                                    "path": field_left,
                                    "query": {

                                        "match": {
                                            search_field: {
                                                "query": search_content,
                                                "fuzziness": "auto"
                                            }
                                        }

                                    }
                                }
                            }
                        ]
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
                },
                "highlight": {
                    "fields": {
                        search_field: {}
                    },
                    "pre_tags": "<font color='red'>",
                    "post_tags": "</font>",
                },
                "track_total_hits": 1000

            }
        else:

            body = {
                "query": {
                    "match": {
                        search_field: {
                            "query": search_content,
                            "fuzziness": "auto"
                        }
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
                },
                "highlight": {
                    "fields": {
                        search_field: {}
                    },
                    "pre_tags": "<font color='red'>",
                    "post_tags": "</font>",
                },
                "track_total_hits": 1000

            }
    else:
        if "." in search_field:
            field_left = ""
            field_right = ""
            index = search_field.find('.')
            if index != -1:
                field_left = search_field[:index]
                field_right = search_field[index + 1:]

            body = {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "nested": {
                                    "path": field_left,
                                    "query": {

                                        "match": {
                                            search_field: {
                                                "query": search_content,
                                                "fuzziness": "auto"
                                            }
                                        }
                                    }
                                }
                            }
                        ]
                    }
                },
                "_source": {
                    "includes": includes
                },
                "highlight": {
                    "fields": {
                        search_field: {}
                    },
                    "pre_tags": "<font color='red'>",
                    "post_tags": "</font>",
                },
                "track_total_hits": 1000
            }
        else:

            # print(search_field)
            body = {
                "query": {
                    "match": {
                        search_field: {
                            "query": search_content,
                            "fuzziness": "auto"
                        }
                    }
                },
                "_source": {
                    "includes": includes
                },
                "highlight": {
                    "fields": {
                        search_field: {}
                    },
                    "pre_tags": "<font color='red'>",
                    "post_tags": "</font>",
                },
                "track_total_hits": 1000

            }
    # print(body)
    res = es.search(index="works", body=body, size=1000)
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
                "works_count",
                "last_known_institution.display_name"]
    if sort_by != "":
        body = {
            "query": {
                "match": {
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
            },
            "highlight": {
                "fields": {
                    search_field: {}
                },
                "pre_tags": "<font color='red'>",
                "post_tags": "</font>",
            },
            "track_total_hits": 1000

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
            "highlight": {
                "fields": {
                    search_field: {}
                },
                "pre_tags": "<font color='red'>",
                "post_tags": "</font>",
            }

        }
    # print(body)
    res = es.search(index="authors", body=body, size=1000)
    res = res['hits']

    return JsonResponse(res, safe=False)


def AuthorFuzzySearch(request):
    search_data = json.loads(request.body.decode('utf-8'))
    # page = search_data.get('page')
    # size = 20
    search_content = search_data.get('search_content')
    search_field = search_data.get('search_field')
    # 
    sort_by = search_data.get('sort_by')
    sort_order = search_data.get('sort_order')
    includes = ["display_name",
                "cited_by_count",
                "works_count",
                "last_known_institution.display_name"]
    if sort_by != "":
        body = {
            "query": {
                "match": {
                    search_field: {
                        "query": search_content,
                        "fuzziness": "auto"
                    }
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
            },
            "highlight": {
                "fields": {
                    search_field: {}
                },
                "pre_tags": "<font color='red'>",
                "post_tags": "</font>",
            }

        }
    else:
        body = {
            "query": {
                "match": {
                    search_field: {
                        "query": search_content,
                        "fuzziness": "auto"
                    }
                }
            },
            # "from": (page - 1) * size,
            # "size": size,
            "_source": {
                "includes": includes
            },
            "highlight": {
                "fields": {
                    search_field: {}
                },
                "pre_tags": "<font color='red'>",
                "post_tags": "</font>",
            }

        }
    # print(body)
    res = es.search(index="authors", body=body, size=1000)
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
    res = es.search(index="works", body=body)['hits']['hits']

    if res:
        res = res[0]
        title = res.get('_source').get('title')
        if Work_Data.objects.filter(work_id=paper_id).exists():
            work_data = Work_Data.objects.get(work_id=paper_id)
            work_data.browse_times += 1
            work_data.save()
        else:
            Work_Data.objects.create(work_id=paper_id, title=title, browse_times=1)
        related_works = res['_source']['related_works']
        referenced_works = res['_source']['referenced_works']
        res['_source']['related_works'] = []
        res['_source']['referenced_works'] = []
        # print(res['_source']['related_works'])
        # print(related_works)
        if related_works:
            # print(related_works)
            i = 0
            for related_work in related_works:
                body2 = {
                    "query": {
                        "term": {
                            "_id": related_work
                        }
                    },
                    "_source": {
                        "includes": ["title", "authorships.author.display_name"]
                    }
                }
                # print(body2)
                res2 = es.search(index="works", body=body2)['hits']['hits']
                # print(res2)
                if res2:
                    res2 = res2[0]
                    related_id = res2['_id']
                    related_title = res2['_source']['title']
                    related_authorships = res2['_source']['authorships']
                    obj = {
                        "id": related_id,
                        "title": related_title,
                        "authorships": related_authorships
                    }
                    res['_source']['related_works'].append(obj)

                    i = i + 1
        if referenced_works:
            # print(related_works)
            i = 0
            for referenced_work in referenced_works:
                body3 = {
                    "query": {
                        "term": {
                            "_id": referenced_work
                        }
                    },
                    "_source": {
                        "includes": ["title", "authorships.author.display_name"]
                    }
                }
                # print(body2)
                res3 = es.search(index="works", body=body3)['hits']['hits']
                # print(res2)
                if res3:
                    res3 = res3[0]
                    referenced_id = res3['_id']
                    referenced_title = res3['_source']['title']
                    referenced_authorships = res3['_source']['authorships']
                    obj = {
                        "id": referenced_id,
                        "title": referenced_title,
                        "authorships": referenced_authorships
                    }
                    res['_source']['referenced_works'].append(obj)

                    i = i + 1

    return JsonResponse(res, safe=False)


def GetAuthorByID(request):
    author_id = request.GET.get('author_id')

    body = {
        "query": {
            "term": {
                "_id": author_id
            }
        }
    }
    res = es.search(index="authors", body=body)['hits']['hits']
    if res:
        res = res[0]
        if Author_User.objects.filter(author_id=author_id).exists():
            res['is_applied'] = True
        else:
            res['is_applied'] = False
    return JsonResponse(res, safe=False)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def favorite_paper(request):
    if request.method == 'POST':
        # 获取被关注的学者的ID
        paper_id = request.POST.get('paper_id')
        paper_name = request.POST.get('article_name')
        response = es.get(index="works", id=paper_id)

        current_favorites_count = response['_source'].get('collected_num', 0)
        print(current_favorites_count)
        new_favorites_count = current_favorites_count + 1
        es.update(
            index="works",
            id=paper_id,
            body={
                "doc": {"collected_num": new_favorites_count},
                "doc_as_upsert": True
            }
        )
        updated_response = es.get(index="works", id=paper_id)
        updated_response = json.dumps(updated_response)
        print(updated_response)

        # 检查用户是否已经收藏了该文章
        if Favorite.objects.filter(user=request.user, article_id=paper_id).exists():
            result = {'result': 1, 'message': r'您已经收藏了该文章'}
            return JsonResponse(result)

        # 创建关注关系

        Favorite.objects.create(user=request.user, article_id=paper_id, article_name=paper_name)



        result = {'result': 0, 'message': r'收藏成功'}
        return JsonResponse(result)
    else:
        result = {'result': 1, 'message': r'无效的请求'}
        return JsonResponse(result)


# https://api.openalex.org/works/W2730267575

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
