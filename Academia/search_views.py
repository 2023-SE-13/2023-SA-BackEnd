import json

import haystack.forms
from django.utils.html import strip_tags
from haystack.views import SearchView
from django.http import JsonResponse
from haystack.utils import Highlighter


class MyHighlighter(Highlighter):
    def highlight(self, text_block):
        self.text_block = strip_tags(text_block)
        highlight_locations = self.find_highlightable_words()
        start_offset, end_offset = self.find_window(highlight_locations)
        if len(text_block) < 3000:
            start_offset = 0
            end_offset = len(text_block)
        return self.render_html(highlight_locations, start_offset, end_offset)


class PaperSearchView(SearchView):
    # 指定搜索结果的模板
    form_class = haystack.forms.SearchForm

    def create_response(self):
        q = self.request.GET.get('q')
        formula = json.loads(q)
        group = formula['group']
        htitle = ""
        habstract = ""
        for i in group:
            for j in i:
                if j['kind'] == 'title':
                    htitle = j['content']
                if j['kind'] == 'abstract':
                    habstract = j['content']
        # # 分页
        # page_size = 10
        # try:
        #     page = int(self.request.GET.get('page', 1))
        # except:
        #     page = 1
        # start = (page - 1) * page_size
        # end = start + page_size

        # 获取查询到的结果
        context = self.get_context()
        # paginator = context['paginator']
        # page_obj = paginator.page(page)
        object_list = context['page'].object_list
        result_list = []
        for i in object_list:
            # 获取结果总数
            # total = paginator.count
            highlight = MyHighlighter(htitle)
            i.object.title = highlight.highlight(i.object.title)
            highlight = MyHighlighter(habstract)
            i.object.abstract = highlight.highlight(i.object.abstract)
            # 获取结果
            result_dict = {}
            result_dict['id'] = i.object.id
            result_dict['title'] = i.object.title
            result_dict['keywords'] = i.object.keywords
            result_dict['citation_count'] = i.object.citation_count
            result_dict['page_start'] = i.object.page_start
            result_dict['page_end'] = i.object.page_end
            result_dict['type'] = i.object.type
            result_dict['language'] = i.object.language
            result_dict['publisher'] = i.object.publisher
            result_dict['volume'] = i.object.volume
            result_dict['issue'] = i.object.issue
            result_dict['issn'] = i.object.issn
            result_dict['isbn'] = i.object.isbn
            result_dict['doi'] = i.object.doi
            result_dict['pdf_link'] = i.object.pdf_link
            result_dict['url'] = i.object.url
            result_dict['abstract'] = i.object.abstract
            result_dict['last_update_time'] = i.object.last_update_time
            result_dict['venue_id'] = i.object.venue_id
            result_list.append(result_dict)

        # 返回结果
        return JsonResponse({'result': result_list})

