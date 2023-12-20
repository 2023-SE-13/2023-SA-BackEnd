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

es = Elasticsearch(hosts='elastic:yXC0ZTAbjmhmyLHb7fBv@116.63.49.180:9200')


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


def BasicSearch(request):
    search_data = json.loads(request.body.decode('utf-8'))
    # print(search_list)

    search_content = search_data.get('search_content')
    search_field = search_data.get('search_field')

    body = {
        "query": {
            "match": {
                search_field: search_content
            }
        }
    }
    # print(body)
    res = es.search(index="paper", body=body)
    return JsonResponse(res)


def MultiSearch(request):
    search_list = json.loads(request.body.decode('utf-8'))
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
        }
    }
    # print(body)
    res = es.search(index="paper", body=body)
    return JsonResponse(res)


def FuzzySearch(request):
    search_data = json.loads(request.body.decode('utf-8'))
    # print(search_list)

    search_content = search_data.get('search_content')
    search_field = search_data.get('search_field')
    body = {
        "query": {
            "fuzzy": {
                search_field: search_content
            }
        }
    }
    # print(body)
    res = es.search(index="paper", body=body)
    return JsonResponse(res)
