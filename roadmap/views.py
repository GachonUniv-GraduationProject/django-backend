from django.shortcuts import render,HttpResponse
import json


# Create your views here.
def add_roadmap(request):
    data = json.loads(request.body)


    return HttpResponse("<h1>check log</h1>")
