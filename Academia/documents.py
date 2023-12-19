from django_elasticsearch_dsl import (
    Document,
    fields,
    Index,
)

from .models import Paper

PUBLISHER_INDEX = Index('paper')

PUBLISHER_INDEX.settings(
    number_of_shards=1,
    number_of_replicas=0
)


@PUBLISHER_INDEX.doc_type
class NewsDocument(Document):

    id = fields.IntegerField(attr='id')
    fielddata = True
    title = fields.TextField(
        fields={
            'keyword': {
                'type': 'keyword',
            }

        }
    )
    keywords = fields.TextField(
        fields={
            'keyword': {
                'type': 'keyword',
            }

        }
    )
    citation_count = fields.IntegerField(attr='citation_count')
    page_start = fields.IntegerField(attr='page_start')
    page_end = fields.IntegerField(attr='page_end')
    type = fields.TextField(
        fields={
            'keyword': {
                'type': 'keyword',
            }

        }
    )
    language = fields.TextField(
        fields={
            'keyword': {
                'type': 'keyword',
            }

        }
    )
    publisher = fields.TextField(
        fields={
            'keyword': {
                'type': 'keyword',
            }

        }
    )
    volume = fields.TextField(
        fields={
            'keyword': {
                'type': 'keyword',
            }

        }
    )
    issue = fields.TextField(
        fields={
            'keyword': {
                'type': 'keyword',
            }

        }
    )
    issn = fields.TextField(
        fields={
            'keyword': {
                'type': 'keyword',
            }

        }
    )
    isbn = fields.TextField(
        fields={
            'keyword': {
                'type': 'keyword',
            }

        }
    )
    doi = fields.TextField(
        fields={
            'keyword': {
                'type': 'keyword',
            }

        }
    )
    pdf_link = fields.TextField(
        fields={
            'keyword': {
                'type': 'keyword',
            }

        }
    )
    url = fields.TextField(
        fields={
            'keyword': {
                'type': 'keyword',
            }

        }
    )
    abstract = fields.TextField(
        fields={
            'keyword': {
                'type': 'keyword',
            }

        }
    )

    venue_id = fields.IntegerField(attr='venue_id')


    class Django(object):
        model = Paper