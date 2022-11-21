from django.http import JsonResponse
from django.shortcuts import HttpResponse
import json
from .models import data, keyword
from .serializers import dataSerializer, keywordSerializer
from rest_framework import viewsets


# Create your views here.
class DataViewSet(viewsets.ModelViewSet):
    queryset = data.objects.all()
    serializer_class = dataSerializer


class KeywordViewSet(viewsets.ModelViewSet):
    queryset = keyword.objects.all()
    serializer_class = keywordSerializer



def test(request):
    return HttpResponse("<h1>mapped</h1>")


def recruit_json(request):
    crawling_data = json.loads(request.body)
    jobs = crawling_data.get('jobPosts')
    print(len(jobs))
    for job in jobs:
        redun_check = data.objects.filter(api_id=job['id'])
        if len(redun_check) == 0:
            temp_data = data.objects.create(company_name=job['companyName'], field=job['field'], career_min=job['careerMin'], api_id=job['id'], position=job['position'])
            crawling_keyword = job['keywordList']
            for temp_key in crawling_keyword:
                temp_read = keyword.objects.filter(name=temp_key['keyword'])
                if len(temp_read) == 0:
                    keyword_objects_create = keyword.objects.create(name=temp_key['keyword'])
                else:
                    keyword_objects_create = keyword.objects.get(name=temp_key['keyword'])
                temp_data.keywords.add(keyword_objects_create)

    return HttpResponse("<h1>check log</h1>")


def crawling_to_json(crawling):
    result = {'company_name': crawling.company_name, 'field': crawling.field, 'careerMin': crawling.career_min, 'api_id' : crawling.id, 'position': crawling.position}
    return result
