from django.db import models


# Create your models here.
class temp(models.Model):
    content = models.TextField()
    title = models.TextField()
    likes = models.IntegerField()
    level = models.IntegerField()
    curriculum = models.TextField()


class test(models.Model):
    content = models.TextField()
    address = models.TextField()
    nickname = models.TextField()


class Person(models.Model):
    name = models.TextField()
    phone = models.TextField()
    addr = models.TextField()
    email = models.TextField()
