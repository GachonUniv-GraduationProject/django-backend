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


def trend(request):

    return JsonResponse({"trend": "test"})


def keyword_update(request):
    # TODO: 우선 취업 공고로부터, 키워드들 다 카운트하고, 디비에 그 값 반영해주기, 그 다음 반영된 카운트 값으로 부터 트렌드 나오게 하면 될듯?
    # update 쿼리는 다음 블로그 참고 : https://eunjin3786.tistory.com/337
    keyword_dict = {}
    queryset = data.objects.all()
    for q in queryset:
        keywords = q.keywords.all()
        for key in keywords:
            if key.name in keyword_dict:
                keyword_dict[key.name] += 1
            else:
                keyword_dict[key.name] = 0

    for key in keyword_dict.keys():
        objects_get = keyword.objects.get(name=key)
        objects_get.count = keyword_dict[key]
        objects_get.save()

    return JsonResponse({"trend": "test"})


def recruit_json(request):
    crawling_data = json.loads(request.body)
    jobs = crawling_data.get('jobPosts')
    print(len(jobs))
    for job in jobs:
        redun_check = data.objects.filter(api_id=job['id'])
        if len(redun_check) == 0:
            temp_data = data.objects.create(company_name=job['companyName'], field=job['field'],
                                            career_min=job['careerMin'], api_id=job['id'], position=job['position'])
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
    result = {'company_name': crawling.company_name, 'field': crawling.field, 'careerMin': crawling.career_min,
              'api_id': crawling.id, 'position': crawling.position}
    return result
