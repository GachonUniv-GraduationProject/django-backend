from django.http import JsonResponse
from django.shortcuts import HttpResponse
import json
from .models import data, keyword, trend
from roadmap.models import skills
from .serializers import dataSerializer, keywordSerializer
from rest_framework import viewsets

# 취업공고의 position을 보고, 거기서부터 필드명을 추출해야할듯?
field_keywords = {
    "Frontend": ["front-end", "frontend", "프론트엔드", "웹",
                 "프론트", "리엑트", "react", "vue"],
    "Backend": ["back-end", "backend", "devops", "백엔드", "서버", "네트워크",
                "웹", "server", "cloud", "데브옵스", "자바", "spring"],
    # "Android": ["안드로이드", "android", "앱"],
    # "Blockchain": ["blockchain", "block-chain", "블록체인"],
    # "AI": ["인공지능", "ai"],
    # "Data Science": ["데이터"],
    # "Machine Learning": ["머신러닝", "머신 러닝", "machine learning", "ml"],
    # "Deep Learning": ["딥러닝", "딥 러닝", "deep learning"],
    # "Data Engineer": ["dba", ],
    # "BigData Engineer": ["빅데이터"],
    # "Game Client": ["unity", "언리얼", "유니티"],
    # "Game Server": ["게임"],
    # "JavaScript": ["javascript", "자바스크립트", "jsp", "js"],
    # "Java": ["java", "자바"],
    # "Python": ["python", "파이썬"],
    # "React": ["react", "리엑트"],
    # "Node.js": ["node", "node.js", "노드"]
}


# Create your views here.
class DataViewSet(viewsets.ModelViewSet):
    queryset = data.objects.all()
    serializer_class = dataSerializer


class KeywordViewSet(viewsets.ModelViewSet):
    queryset = keyword.objects.all()
    serializer_class = keywordSerializer


def get_field(request):
    query = trend.objects.values_list('field_name', flat=True)
    result = {"fields": []}
    for q in query:
        if q not in result["fields"]:
            result["fields"].append(q)

    return JsonResponse(result)


def get_trend(request, field):
    query_trend = trend.objects.filter(field_name=field)
    query_roadmap = skills.objects.filter(field=field)
    roadmap_result = {}
    for q in query_roadmap:
        if q.base is None:
            roadmap_result[q.name] = {"base": q.field, "child": []}
        else:
            if q.base.name in roadmap_result.keys():
                roadmap_result[q.name] = {"base": q.base.name, "child": []}
                roadmap_result[q.base.name]["child"].append(q.name)

        print(q)
    result = {}
    for q in query_trend:
        for kw in q.keywords.all():
            for roadmap_key in roadmap_result.keys():
                split_list = roadmap_key.split()
                for split in split_list:
                    if kw.name in split and len(kw.name) > 1:
                        if roadmap_result[roadmap_key]["base"] in result:
                            if kw.name in result[roadmap_result[roadmap_key]["base"]].keys():
                                result[roadmap_result[roadmap_key]["base"]][kw.name] += 1
                            else:
                                result[roadmap_result[roadmap_key]["base"]][kw.name] = 1
                        else:
                            result[roadmap_result[roadmap_key]["base"]] = {}
                            result[roadmap_result[roadmap_key]["base"]][kw.name] = 1

            # if kw.name not in result:
            #     result[kw.name] = 1
            # else:
            #     result[kw.name] += 1
    return JsonResponse(result)


def test(request):
    return HttpResponse("<h1>mapped</h1>")


def trend_update(request):
    crawling_datas = data.objects.all()
    redun_check = {}
    for crawling_data in crawling_datas:
        split_list = crawling_data.position.split()
        print(split_list)
        for field in field_keywords.keys():
            redun_check[field] = False
        for word in split_list:
            for field in field_keywords.keys():
                for kw in field_keywords[field]:
                    if kw in word and not redun_check[field]:
                        for key in crawling_data.keywords.all():
                            temp_trend = trend.objects.create(field_name=field)
                            temp_read = keyword.objects.filter(name=key.name)
                            if len(temp_read) == 0:
                                add_key = keyword.objects.create(name=key.name)
                            else:
                                add_key = keyword.objects.get(name=key.name)
                            temp_trend.keywords.add(add_key)
                        redun_check[field] = True
                    elif redun_check[field]:
                        break

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
                keyword_dict[key.name] = 1

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
