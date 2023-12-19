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
        print("===searching===")
        if not self.is_valid():
            print("invalid")
            return self.no_query_found()
        formula = json.loads(self.cleaned_data['q'])
        sorttype = self.cleaned_data['sorttype']
        need = self.cleaned_data['need']
        print(sorttype)

        dates = formula['dates']
        group = formula['group']
        print("开始时间:" + dates[0])
        print("结束时间:" + dates[1])
        print("有" + str(len(group)) + "组或")
        # sqs=SearchQuerySet().filter(title='internet development').load_all()
        # return sqs
        in_filter = ""
        for i in group:
            following = "("
            for j in i:
                if j['kind'] == 'topic':
                    j['kind'] = 'title'
                following2 = "SQ(" + j['kind'] + "='" + j['content'] + "')"
                following = following + following2 + "&"
            following = following[:-1]
            following = following + ")|"
            in_filter = in_filter + following
        in_filter = in_filter[:-1]
        # print(in_filter)
        command = "sqs=SearchQuerySet().filter(" + in_filter + ")"
        if dates[0]:
            command += ".filter(year__gte="
            command += "(" + dates[0][0:4] + "))"
        if dates[1]:
            command += ".filter(year__lte="
            command += "(" + dates[1][0:4] + "))"
        if sorttype == "3":
            command += ".order_by('-n_citation')"
        elif sorttype == "4":
            command += ".order_by('n_citation')"
        elif sorttype == "7":
            command += ".order_by('-year')"
        elif sorttype == "8":
            command += ".order_by('year')"
        # else:
        #     command="sqs=SearchQuerySet().filter("+in_filter+")"
        print(command)
        d = {}
        exec(command, globals(), d)
        sqs = d['sqs']

        sqs = sqs.load_all().highlight()
        print("查询到" + str(sqs.count()) + "个结果")
        # if (need=="1"):
        #     print("need")
        #     author_to_essay={}
        #     publisher_to_essay={}
        #     year_to_essay={}
        #     key_to_essay={}
        #     org_to_essay={}
        #     for i in sqs:
        #         try :
        #             arrauth =  eval('(' + i.object.auth + ')')
        #             if arrauth!=-1:
        #                 for j in arrauth:

        #                     if j["name"] not in author_to_essay.keys():
        #                         author_to_essay.update({j["name"]:1})
        #                     else:
        #                         author_to_essay[j["name"]]+=1
        #                     if j["org"] not in org_to_essay.keys():
        #                         org_to_essay.update({j["org"]:1})
        #                     else:
        #                         org_to_essay[j["org"]]+=1
        #             arrkey =  eval('(' + i.object.keywords + ')')
        #             if arrkey!=-1:
        #                 for j in arrkey:
        #                     if j not in key_to_essay.keys():
        #                         key_to_essay.update({j:1})
        #                     else:
        #                         key_to_essay[j]+=1

        #             if i.object.year not in year_to_essay.keys():
        #                 year_to_essay.update({i.object.year:1})
        #             else:
        #                 year_to_essay[ i.object.year]+=1

        #             if i.object.publisher not in publisher_to_essay.keys():
        #                 publisher_to_essay.update({i.object.publisher:1})
        #             else:
        #                 publisher_to_essay[ i.object.publisher]+=1
        #         except Exception as e :
        #             pass
        #     imsb1.author_to_essay=sorted(author_to_essay.items(), key = lambda x:x[1], reverse = True)[0:20]
        #     imsb1.key_to_essay=sorted(key_to_essay.items(), key = lambda x:x[1], reverse = True)[0:20]
        #     imsb1.year_to_essay=sorted(year_to_essay.items(), key = lambda x:x[1], reverse = True)[0:20]
        #     imsb1.org_to_essay=sorted(org_to_essay.items(), key = lambda x:x[1], reverse = True)[0:20]
        # else:
        #     print("noneed")
        #     imsb1.author_to_essay=[]
        #     imsb1.key_to_essay=[]
        #     imsb1.year_to_essay=[]
        #     imsb1.org_to_essay=[]

        return sqs
