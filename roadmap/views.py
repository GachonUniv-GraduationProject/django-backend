from django.shortcuts import render,HttpResponse
import json
from .models import JavaScript,js_url


# Create your views here.
def add_roadmap(request):
    data = json.loads(request.body)
#    print(data['JavaScript'])
#    print(data['URL'])
    for skill in data['JavaScript']:
        if len(JavaScript.objects.filter(skill_name=skill['baseSkill'])) == 0:
            base_skill = JavaScript.objects.create(skill_name=skill['baseSkill'])
        else:
            base_skill = JavaScript.objects.get(skill_name=skill['baseSkill'])
        skill = JavaScript.objects.create(skill_name=skill['skill'])
        base_skill.child.add(skill)

    for url in data['URL']:
        create_url = js_url.objects.create(link=url['URL'], link_name=url['title'], skill_id=JavaScript.objects.get(skill_name=url['skill']).pk)
    return HttpResponse("<h1>check log</h1>")
