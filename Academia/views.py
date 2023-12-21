# Create your views here.
import requests
from django.http import JsonResponse
from django_elasticsearch_dsl_drf.filter_backends import (
    CompoundSearchFilterBackend
)
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    OrderingFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from elasticsearch.client import Elasticsearch

from .serializers import *

es = Elasticsearch(hosts='elastic:yXC0ZTAbjmhmyLHb7fBv@116.63.49.180:9200')


# def generate_random_data():
#     url = 'http://localhost:3000/data'
#     r = requests.get(url)
#     payload = json.loads(r.text)
#     count = 1
#
#     # print (payload)
#     print("type of payload is: ", type(payload))
#     for data in payload:
#         # pass
#
#         Paper.objects.create(
#             title=data['title'],
#             keywords=data['keywords'],
#             citation_count=data['citation_count'],
#             page_start=data['page_start'],
#             page_end=data['page_end'],
#             type=data['type'],
#             language=data['language'],
#             publisher=data['publisher'],
#             volume=data['volume'],
#             issue=data['issue'],
#             issn=data['issn'],
#             isbn=data['isbn'],
#             doi=data['doi'],
#             pdf_link=data['pdf_link'],
#             url=data['url'],
#             abstract=data['abstract'],
#             venue_id=data['venue_id'],
#
#         )


# def index(request):
#     generate_random_data()
#     return JsonResponse({'status': 200})
#     # return HttpResponse("Hello, the world")


# class PublisherDocumentView(DocumentViewSet):
#     document = NewsDocument
#     serializer_class = NewsDocumentSerializer
#     lookup_field = 'title'
#     fielddata = True
#     filter_backends = [
#         FilteringFilterBackend,
#         OrderingFilterBackend,
#         CompoundSearchFilterBackend,
#     ]
#
#     search_fields = (
#         'title',
#
#     )
#     multi_match_search_fields = (
#         'title',
#
#     )
#     filter_fields = {
#         'title': 'title',
#
#     }
#     ordering_fields = {
#         'id': None,
#     }
#     ordering = ('id',)


def BasicSearch(request):
    search_data = json.loads(request.body.decode('utf-8'))
    # print(search_list)
    # page = search_data.get('page')
    # size = 20
    search_content = search_data.get('search_content')
    search_field = search_data.get('search_field')
    sort_by = search_data.get('sort_by')
    sort_order = search_data.get('sort_order')
    includes = ["title",
                "publication_date",
                "authorships.author.display_name"]
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
    # print(body)
    res = es.search(index="papers", body=body)
    res = res['hits']['hits']
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
    # print(body)
    res = es.search(index="papers", body=body)
    return JsonResponse(res)


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
    # print(body)
    res = es.search(index="papers", body=body)
    res = res['hits']['hits']
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
