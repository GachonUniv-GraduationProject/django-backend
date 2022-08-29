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
    haebin = {"Frontend","Backend","Android","Blockchain"}
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
                        skill = skills.objects.create(name=skill['skill'], base_id=base_skill[len(base_skill)-1].pk,
                                                      field=key)

            else:
                if key in haebin:
                    target_skill = skills.objects.filter(name=skill['baseSkill'])
                    for target in target_skill:
                        if 'title' in skill.keys():
                            create_url = url.objects.create(link=skill['URL'], link_name=skill['title'], skill_id=target.pk)
                        else:
                            create_url = url.objects.create(link=skill['URL'], link_name="default", skill_id=target.pk)
                else:
                    target_skill = skills.objects.filter(name=skill['skill'])
                    for target in target_skill:
                        if 'title' in skill.keys():
                            create_url = url.objects.create(link=skill['URL'], link_name=skill['title'], skill_id=target.pk)
                        else:
                            create_url = url.objects.create(link=skill['URL'], link_name="default", skill_id=target.pk)
    return HttpResponse("<h1>check log</h1>")
