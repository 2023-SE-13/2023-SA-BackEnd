import json
from .models import Paper

from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from .documents import *


class NewsDocumentSerializer(DocumentSerializer):
    class Meta(object):
        """Meta options."""
        model = Paper
        document = NewsDocument
        fields = (
            'title',
            'content',
            'keywords',
            'citation_count',
            'page_start',
            'page_end',
            'type',
            'language',
            'publisher',
            'volume',
            'issue',
            'issn',
            'isbn',
            'doi',
            'pdf_link',
            'url',
            'abstract',
            'last_update_time',
            'venue_id',

        )

        def get_location(self, obj):
            """Represent location value."""
            try:
                return obj.location.to_dict()
            except:
                return {}