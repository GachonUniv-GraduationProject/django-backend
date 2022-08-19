from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
import random
import json


# Create your views here.
def recruit_json(request):
    data = json.loads(request.body)
    jobs = data.get('jobs')
    print(jobs.keys())
    # print(jobs['count'])
    # print(jobs['start'])
    # print(jobs['total'])
    job_list = jobs['job']
    print(job_list[0].keys())
    # print(len(job_list))
    # for job in job_list:
    #     print(job['company'])
    #     print(job['position'])
    #     print(job['keyword'])
    #     print(job['expiration-timestamp'])
    print(job_list[0]['company']['detail']['name'])
    print(job_list[0]['position']['title'])
    print(job_list[0]['position']['industry']['name'])
    print(job_list[0]['position']['job-mid-code']['name'])
    print(job_list[0]['position']['job-code']['name'])
    print(job_list[0]['position']['experience-level']['name'])
    print(job_list[0]['position']['required-education-level']['name'])
    print(job_list[0]['keyword'])
    print(job_list[0]['expiration-timestamp'])
    return HttpResponse("<h1>crawling page</h1>")
