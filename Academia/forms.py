import json

from django import forms
from haystack.forms import SearchForm
from .models import Paper
from haystack.query import SearchQuerySet


class KeywordSearchForm(SearchForm):
    sorttype = forms.CharField(required=False)
    need = forms.CharField(required=False)
    formula = forms.CharField(required=False)

    def search(self):
        if not self.is_valid():
            return self.no_query_found()
        formula = json.loads(self.cleaned_data['q'])
        sorttype = self.cleaned_data['sorttype']
        need = self.cleaned_data['need']

        dates = formula['dates']
        group = formula['group']
