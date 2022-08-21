from django.db import models


# Create your models here.

class keyword(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    count = models.IntegerField(default=0)


class data(models.Model):
    company_name = models.CharField(max_length=100, null=False, blank=False)
    position = models.CharField(max_length=100, null=False, blank=False)
    field = models.CharField(max_length=100, null=False, blank=False)
    career_min = models.IntegerField(default=0)
    api_id = models.IntegerField(default=0)
    keywords = models.ManyToManyField(keyword)
