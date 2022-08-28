from django.shortcuts import render,HttpResponse
import json
from .models import JavaScript,js_url, skills, url


# Create your views here.
def add_roadmap_test(request):
    data = json.loads(request.body)
#    print(data['JavaScript'])
#    print(data['URL'])
    for skill in data['JavaScript']:
        if len(JavaScript.objects.filter(skill_name=skill['baseSkill'])) == 0:
            base_skill = JavaScript.objects.create(skill_name=skill['baseSkill'])
        else:
            base_skill = JavaScript.objects.get(skill_name=skill['baseSkill'])
        skill = JavaScript.objects.create(skill_name=skill['skill'], base_id=base_skill.pk)

    for url in data['URL']:
        create_url = js_url.objects.create(link=url['URL'], link_name=url['title'], skill_id=JavaScript.objects.get(skill_name=url['skill']).pk)
    return HttpResponse("<h1>check log</h1>")


def add_roadmap(request):
    data = json.loads(request.body)
    for key in data.keys():
        print(key)
        for skill in data[key]:
            if skill['index'] == "-1":
                if len(skills.objects.filter(name=skill['skill'])) == 0:
                    base_skill = skills.objects.create(name=skill['skill'])
                else:
                    base_skill = skills.objects.get(skill_name=skill['baseSkill'])
                skill = skills.objects.create(name=skill['skill'], base_id=base_skill.pk, field=key)
            else:
                create_url = url.objects.create(link=skill[''])
    return HttpResponse("<h1>check log</h1>")