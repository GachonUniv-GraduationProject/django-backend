from django.db import models


# Create your models here.

class keyword(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)


class data(models.Model):
    company_name = models.CharField(max_length=100, null=False, blank=False)
    position = models.CharField(max_length=100, null=False, blank=False)
    field = models.CharField(max_length=100, null=False, blank=False)
    experience_level = models.CharField(max_length=100, null=False, blank=False)
    expiration = models.CharField(max_length=100, null=False, blank=False)
    keywords = models.ManyToManyField(keyword)
