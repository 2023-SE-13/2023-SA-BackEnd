# Create your views here.
from django.http import JsonResponse
from elasticsearch.client import Elasticsearch
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated

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
    res = es.search(index="papers", body=body)
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
    res = es.search(index="papers", body=body)
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
    res = es.search(index="papers", body=body)
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
    res = es.search(index="papers", body=body)['hits']['hits'][0]
    return JsonResponse(res, safe=False)


