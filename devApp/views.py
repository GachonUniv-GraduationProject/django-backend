from django.shortcuts import render, HttpResponse
import random
from .models import temp, test


# Create your views here.
def index(request):
    return render(request, "index.html")


def create(request):
    return HttpResponse("<h1>Welcome! Random</h1>"+str(random.random())+"<h1>update test</h1>")


def read(request, id):
    test_list = temp.objects.all()
    result = ""
    for test in test_list:
        result += test.curriculum+" "
    return HttpResponse("Read "+id+" result "+result)


def add(request, name, content):
    address = "gachon univ"
    test.objects.create(nickname=name, content=content, address=address)
    return HttpResponse("<h1>new member added</h1>")

def test_read(request):
    test_list = test.objects.all()
    result = ""
    for temp in test_list:
        result += "<h3>"+temp.nickname+" : "+temp.content+" : "+temp.address+"</h3>"

    return HttpResponse("<h1>test</h1> "+result)

