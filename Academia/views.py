from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

# Create your views here.
from django.http import JsonResponse
import requests
import json

from django.views import View
from elasticsearch.client import Elasticsearch
from rest_framework.views import APIView

import SA_backend.settings
from SA_backend.models import *

from .documents import *
from .serializers import *

from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    CompoundSearchFilterBackend
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    OrderingFilterBackend,
)


def generate_random_data():
    url = 'http://localhost:3000/data'
    r = requests.get(url)
    payload = json.loads(r.text)
    count = 1

    # print (payload)
    print("type of payload is: ", type(payload))
    for data in payload:
        # pass

        Paper.objects.create(
            title=data['title'],
            keywords=data['keywords'],
            citation_count=data['citation_count'],
            page_start=data['page_start'],
            page_end=data['page_end'],
            type=data['type'],
            language=data['language'],
            publisher=data['publisher'],
            volume=data['volume'],
            issue=data['issue'],
            issn=data['issn'],
            isbn=data['isbn'],
            doi=data['doi'],
            pdf_link=data['pdf_link'],
            url=data['url'],
            abstract=data['abstract'],
            venue_id=data['venue_id'],

        )


def index(request):
    generate_random_data()
    return JsonResponse({'status': 200})
    # return HttpResponse("Hello, the world")


class PublisherDocumentView(DocumentViewSet):
    document = NewsDocument
    serializer_class = NewsDocumentSerializer
    lookup_field = 'title'
    fielddata = True
    filter_backends = [
        FilteringFilterBackend,
        OrderingFilterBackend,
        CompoundSearchFilterBackend,
    ]

    search_fields = (
        'title',

    )
    multi_match_search_fields = (
        'title',

    )
    filter_fields = {
        'title': 'title',

    }
    ordering_fields = {
        'id': None,
    }
    ordering = ('id',)


def MySearchView(request):
    search_msg = request.POST.get('search_msg')
    search_index = request.POST.get('search_index')
    return JsonResponse(filter_msg(search_msg, search_index))


def filter_msg(search_msg, search_index): # 搜索diplayed_name
    es = Elasticsearch(hosts='elastic:yXC0ZTAbjmhmyLHb7fBv@116.63.49.180:9200')

    body = {
        "query": {
            "match": {
                "display_name": search_msg
            }
        },
        "size": 5,  # 设置最大的返回值
    }
    res = es.search(index=search_index, body=body)
    return res
