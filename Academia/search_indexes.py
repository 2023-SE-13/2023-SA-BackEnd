from haystack import indexes
from .models import *


class PaperIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    id = indexes.CharField(model_attr='id')
    title = indexes.TextField(model_attr='title')
    keywords = indexes.TextField(model_attr='keywords')
    citation_count = indexes.IntegerField(model_attr='citation_count')
    page_start = indexes.IntegerField(model_attr='page_start')
    page_end = indexes.IntegerField(model_attr='page_end')
    type = indexes.CharField(model_attr='type')
    language = indexes.CharField(model_attr='language')
    publisher = indexes.CharField(model_attr='publisher')
    volume = indexes.CharField(model_attr='volume')
    issue = indexes.CharField(model_attr='issue')
    issn = indexes.CharField(model_attr='issn')
    isbn = indexes.CharField(model_attr='isbn')
    doi = indexes.CharField(model_attr='doi')
    pdf_link = indexes.CharField(model_attr='pdf_link')
    url = indexes.CharField(model_attr='url')
    abstract = indexes.TextField(model_attr='abstract')
    last_update_time = indexes.DateTimeField(model_attr='last_update_time')
    venue_id = indexes.IntegerField(model_attr='venue_id')

    content_auto = indexes.EdgeNgramField(model_attr='title')  # 指定搜索字段

    def get_model(self):
        # 需要建立索引的模型
        return Paper

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class PatentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    id = indexes.CharField(model_attr='id')
    title = indexes.TextField(model_attr='title')
    keywords = indexes.TextField(model_attr='keywords')
    citation_count = indexes.IntegerField(model_attr='citation_count')
    page_start = indexes.IntegerField(model_attr='page_start')
    page_end = indexes.IntegerField(model_attr='page_end')
    type = indexes.CharField(model_attr='type')
    language = indexes.CharField(model_attr='language')
    publisher = indexes.CharField(model_attr='publisher')
    volume = indexes.CharField(model_attr='volume')
    issue = indexes.CharField(model_attr='issue')
    issn = indexes.CharField(model_attr='issn')
    isbn = indexes.CharField(model_attr='isbn')
    doi = indexes.CharField(model_attr='doi')
    pdf_link = indexes.CharField(model_attr='pdf_link')
    url = indexes.CharField(model_attr='url')
    abstract = indexes.TextField(model_attr='abstract')
    last_update_time = indexes.DateTimeField(model_attr='last_update_time')
    venue_id = indexes.IntegerField(model_attr='venue_id')

    content_auto = indexes.EdgeNgramField(model_attr='title')  # 指定搜索字段

    def get_model(self):
        # 需要建立索引的模型
        return Patent

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

