from django.http import JsonResponse
from django.shortcuts import HttpResponse
import json
from .models import data, keyword


# Create your views here.
def recruit_json(request):
    crawling_data = json.loads(request.body)
    jobs = crawling_data.get('jobPosts')
    temp_data = data.objects.create(company_name=jobs[0]['companyName'], field=jobs[0]['field'], career_min=jobs[0]['careerMin'], api_id=jobs[0]['id'])
    crawling_keyword = jobs[0]['keywordList']
    print(temp_data)
    print(crawling_keyword)
    for temp_k in crawling_keyword:
        print(temp_k['keyword'])
        temp_read = keyword.objects.filter(name=temp_k['keyword'])
        if len(temp_read) == 0:
            keyword_objects_create = keyword.objects.create(name=temp_k['keyword'])
        temp_read = keyword.objects.filter(name=temp_k['keyword'])
        recruit = data.objects.get(pk=temp_data.pk)
        recruit.keywords.add(keyword_objects_create)
        print(len(temp_read))
    return HttpResponse("<h1>crawling page</h1>")
