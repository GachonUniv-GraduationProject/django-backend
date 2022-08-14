from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
import random
import json


# Create your views here.
from rest_framework.response import Response

from devApp.models import temp, test, Person
from devApp.serializers import BasePersonSerializer


def index(request):
    return render(request, "index.html")


def create(request):
    return HttpResponse("<h1>Welcome! Random</h1>"+str(random.random())+"<h1>update test</h1>")


def read(request):
    test_list = temp.objects.all()
    id = request.GET['id']
    result = ""
    for test in test_list:
        result += test.curriculum+" "
    return HttpResponse("Read "+id+" result "+result)


def add(request):

    address = "gachon univ"
    name = request.GET['name']
    content = request.GET['content']
    test.objects.create(nickname=name, content=content, address=address)
    return HttpResponse("<h1>new member added</h1>")


def test_read(request):
    test_list = test.objects.all()
    result = ""
    for temp in test_list:
        result += "<h3>"+temp.nickname+" : "+temp.content+" : "+temp.address+"</h3>"

    return HttpResponse("<h1>test</h1> "+result)


def json_add(request):
    # body = json.loads(request.body.decode("utf-8"))
    print(request.body)
    # print(body)
    # name = body['name']
    # phone = body['phone']
    # addr = body['addr']
    # email = body['email']
    # Person.objects.create(name=name, phone=phone, addr=addr, email=email)
    # return HttpResponse("<h1>"+name+" "+phone+" "+addr+" "+email+"</h1>")
    return HttpResponse(request.body)


def json_test(request):
    persons = Person.objects.all()
    result = ""
    for temp in persons:
        result += "<h3>" + temp.name + " : " + temp.phone + " : " + temp.addr +" : "+temp.email+"</h3>"

    return HttpResponse("<h1>test</h1> " + result)


def json_find(request):
    id = int(request.GET['id'])
    persons = Person.objects.all()
    if id >= len(persons):
        return HttpResponse("<h1>Not found</h1>")
    else:
        result = Person.objects.get(name=persons[id].name)
        serializer = BasePersonSerializer(result)
        return JsonResponse(serializer.data)

