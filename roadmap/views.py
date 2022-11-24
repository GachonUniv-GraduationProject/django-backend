from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
import json
from .models import skills, url
from .serializers import skillSerializer, urlSerializer
from rest_framework import viewsets


# Create your views here.
class SkillViewSet(viewsets.ModelViewSet):
    queryset = skills.objects.all()
    serializer_class = skillSerializer


class UrlViewSet(viewsets.ModelViewSet):
    queryset = url.objects.all()
    serializer_class = urlSerializer


def get_fields(request):
    query = skills.objects.values_list('field', flat=True)
    result = {"fields": []}
    for q in query:
        if q not in result["fields"]:
            result["fields"].append(q)

    return JsonResponse(result)


def get_dict(request, field):
    query = skills.objects.filter(field=field)
    result = {}
    # temp = {}
    # check = [temp]
    for q in query:

        if q.base == None:
            result[q.name] = {"base":q.field,"child":[]}
        else:
            if q.base.name in result.keys():
                result[q.name] = {"base":q.base.name, "child":[]}
                result[q.base.name]["child"].append(q.name)

        print(q)
    # temp["1"] = 1
    # print(check)
    return JsonResponse(result)


def add_roadmap(request):
    data = json.loads(request.body.decode('utf-8'))
    haebin = {"Frontend", "Backend", "Android", "Blockchain"}
    for key in data.keys():
        print(key)
        for skill in data[key]:
            if skill['index'] != "-1":
                if len(skills.objects.filter(name=skill['baseSkill'], field=key)) == 0:
                    base_skill = skills.objects.create(name=skill['baseSkill'], field=key)
                    skill = skills.objects.create(name=skill['skill'], base_id=base_skill.pk, field=key)
                else:
                    base_skill = skills.objects.filter(name=skill['baseSkill'], field=key)
                    if len(base_skill) == 0:
                        skill = skills.objects.create(name=skill['skill'], base_id=base_skill.pk, field=key)
                    else:
                        skill = skills.objects.create(name=skill['skill'], base_id=base_skill[len(base_skill) - 1].pk,
                                                      field=key)

            else:
                if key in haebin:
                    target_skill = skills.objects.filter(name=skill['baseSkill'], field=key)
                    for target in target_skill:
                        if 'title' in skill.keys():
                            create_url = url.objects.create(link=skill['URL'], link_name=skill['title'],
                                                            skill_id=target.pk)
                        else:
                            create_url = url.objects.create(link=skill['URL'], link_name="default", skill_id=target.pk)
                else:
                    if "URL" in key:
                        target_skill = skills.objects.filter(name=skill['skill'], field=skill['field'])
                    else:
                        target_skill = skills.objects.filter(name=skill['skill'], field=key)
                    for target in target_skill:
                        if 'title' in skill.keys():
                            create_url = url.objects.create(link=skill['URL'], link_name=skill['title'],
                                                            skill_id=target.pk)
                        else:
                            create_url = url.objects.create(link=skill['URL'], link_name="default", skill_id=target.pk)
    return HttpResponse("<h1>check log</h1>")
