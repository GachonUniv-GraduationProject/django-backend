from django.http import JsonResponse
from django.shortcuts import HttpResponse
import json
from .models import data, keyword


# Create your views here.
def recruit_json(request):
    crawling_data = json.loads(request.body)
    jobs = crawling_data.get('jobPosts')
    print(jobs[0])
    print(type(jobs[0]))
    print(jobs[0].keys())
    temp_data = data
    temp_data.company_name = jobs[0]['companyName']
    temp_data.field = jobs[0]['field']
    temp_data.career_min = jobs[0]['careerMin']
    temp_data.position = jobs[0]['position']
    print(temp_data.company_name)
    print(temp_data.field)
    print(temp_data.career_min)
    print(temp_data.position)
    crawling_keyword = jobs[0]['keywordList']
    print(crawling_keyword)
    for temp_k in crawling_keyword:
        key = keyword
        key.name = temp_k['keyword']
        print(key.name)

    return HttpResponse("<h1>crawling page</h1>")
