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
trend_to_return = {}
FrontendSkill = {
    "기술": {
        "HTML": {"count": 0},
        "CSS": {"count": 0},
        "Javascript": {"count": 0},
        "Flutter": {"count": 0},
        "NativeScript": {"count": 0},
        "React Native": {"count": 0},
        "React": {"count": 0}
    },
    "프레임워크": {
        "Electron": {"count": 0},
        "Tauri": {"count": 0},
        "Next.js": {"count": 0},
        "Nuxt.js": {"count": 0},
        "Jest": {"count": 0},
        "Cypress": {"count": 0},
        "Enzyme": {"count": 0},
        "PWA": {"count": 0},
        "Angular": {"count": 0},
        "Vue.js": {"count": 0},
        "Bootstrap": {"count": 0},
        "Bulma": {"count": 0},
        "Tailwind CSS": {"count": 0},
        "Chakra UI": {"count": 0},
        "Material UI": {"count": 0},
        "Radix UI": {"count": 0}
    },
    "기타": {
        "Vuepress": {"count": 0},
        "Jekyll": {"count": 0},
        "Hugo": {"count": 0},
        "Gridsome": {"count": 0},
        "Eleventy": {"count": 0},
        "GatsbyJS": {"count": 0},
        "React Testing Library": {"count": 0}
    }

}
trend_to_return["Frontend"] = FrontendSkill


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


def get_trend_new(request, field):
    query_trend = trend.objects.filter(field_name=field)
    result = trend_to_return[field].copy()
    for q in query_trend:
        for bunya in result:
            for kw in q.keywords.all():
                if kw.name in result[bunya]:
                    result[bunya][kw]["count"] = kw.count

    return JsonResponse(result)


def get_trend(request, field):
    # 분야에 대한 트렌드 객체 긁어옴,
    query_trend = trend.objects.filter(field_name=field)
    # 분야에 대한 로드맵 정보 긁어옴
    query_roadmap = skills.objects.filter(field=field)
    roadmap_result = {}
    # 로드맵을 딕셔너리 구조로 만들어 놓는듯??
    for q in query_roadmap:
        # 부모가 없는 경우
        if q.base is None:
            roadmap_result[q.name] = {"base": q.field, "child": []}
        # 부모가 있는 경우
        else:
            if q.base.name in roadmap_result.keys():
                roadmap_result[q.name] = {"base": q.base.name, "child": []}
                roadmap_result[q.base.name]["child"].append(q.name)

        print(q)
    result = {}
    # 트렌드에 대해서
    for q in query_trend:
        # 트렌드랑 연관된 키워드를 긁어옴,
        for kw in q.keywords.all():
            # 위에서 만든 로드맵 딕셔너리에 키 값에 대해서,
            for roadmap_key in roadmap_result.keys():
                split_list = roadmap_key.split()
                for split in split_list:
                    # 만약 키워드의 이름이 로드맵 이름에 포함된다면,
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
    # 크롤링 데이터 다 가져옴
    crawling_datas = data.objects.all()
    redun_check = {}
    for crawling_data in crawling_datas:
        # 크롤링 데이터에서 직군 스트링을 split함
        split_list = crawling_data.position.split()
        print(split_list)
        for field in field_keywords.keys():
            redun_check[field] = False
        # 직군 split한 것에 대해서
        for word in split_list:
            # 현재는 field = Frontend, Backend가 끝임
            for field in field_keywords.keys():
                # Frontend, Backend 내부 키워드랑 겹치는게 있는지 확인
                for kw in field_keywords[field]:
                    # 만약 키워드가 직군 split한 것에 있고, 그 분야가 중복되지 않으면,
                    if kw in word and not redun_check[field]:
                        for key in crawling_data.keywords.all():
                            # 트렌드 객체를 생성,
                            temp_trend = trend.objects.create(field_name=field)
                            temp_read = keyword.objects.filter(name=key.name)
                            # 키워드와 트렌드 객체 매핑
                            if len(temp_read) == 0:
                                add_key = keyword.objects.create(name=key.name)
                            else:
                                add_key = keyword.objects.get(name=key.name)
                            temp_trend.keywords.add(add_key)
                        redun_check[field] = True
                    elif redun_check[field]:
                        break

    return JsonResponse({"trend": "test"})


# 키워드 호출 횟수 업데이트
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
