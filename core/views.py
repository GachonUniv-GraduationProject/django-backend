from django.shortcuts import render


# 인덱스 페이지 리턴
def index(request):
    return render(request, "index.html")
