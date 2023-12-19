import json



from forms import KeywordSearchForm
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
    form_class = KeywordSearchForm

    def create_response(self):
        print("======in response======")
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
        print(len(self.results))
        object_list = context['page'].object_list
        result_list = []
        for i in object_list:
            try:
                # total = paginator.count
                highlight = MyHighlighter(htitle)
                i.object.title = highlight.highlight(i.object.title)
                highlight = MyHighlighter(habstract)
                i.object.abstract = highlight.highlight(i.object.abstract)
                # 获取结果
                paper_dict = {}
                paper_dict['id'] = i.object.id
                paper_dict['title'] = i.object.title
                paper_dict['keywords'] = i.object.keywords
                paper_dict['citation_count'] = i.object.citation_count
                paper_dict['page_start'] = i.object.page_start
                paper_dict['page_end'] = i.object.page_end
                paper_dict['type'] = i.object.type
                paper_dict['language'] = i.object.language
                paper_dict['publisher'] = i.object.publisher
                paper_dict['volume'] = i.object.volume
                paper_dict['issue'] = i.object.issue
                paper_dict['issn'] = i.object.issn
                paper_dict['isbn'] = i.object.isbn
                paper_dict['doi'] = i.object.doi
                paper_dict['pdf_link'] = i.object.pdf_link
                paper_dict['url'] = i.object.url
                paper_dict['abstract'] = i.object.abstract
                paper_dict['last_update_time'] = i.object.last_update_time
                paper_dict['venue_id'] = i.object.venue_id
                result_list.append(paper_dict)
            except Exception:
                print('error in for_loop')
        print(len(result_list))
        result_list = {}
        result_list['num'] = len(self.results)  # math.ceil((len(self.results))/20)
        result_list['data'] = result_list
        # result_list['author_to_essay']=imsb1.author_to_essay
        # result_list['key_to_essay']=imsb1.key_to_essay
        # result_list['year_to_essay']=imsb1.year_to_essay
        # result_list['org_to_essay']=imsb1.org_to_essay
        return JsonResponse(result_list, safe=False)
        # 返回结果


# my_text = 'This is a sample block that would be more meaningful in real life.'
# my_query = 'block meaningful'
