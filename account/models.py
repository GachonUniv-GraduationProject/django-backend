# api/models.py
from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_pk = models.IntegerField(blank=True)
    display_name = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=200, blank=True)
    is_individual = models.BooleanField(default=True)
    open_to_company = models.BooleanField(default=True)


class Experience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_pk = models.IntegerField(default=0)
    field = models.CharField(max_length=200)
    preference = models.IntegerField()
    detail = models.CharField(max_length=500)


class Roadmap(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_pk = models.IntegerField(blank=True, default=-1)
    field_name = models.CharField(max_length=200, blank=True)
    progress = models.CharField(max_length=200, blank=True)


class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_pk = models.IntegerField(blank=True, default=-1)
    company_name = models.CharField(max_length=200, blank=True)
    recommend_users = models.ManyToManyField(Profile)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, user_pk=instance.id)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=User)
def create_user_roadmap(sender, instance, created, **kwargs):
    if created:
        Roadmap.objects.create(user=instance, user_pk=instance.id)


@receiver(post_save, sender=User)
def save_user_roadmap(sender, instance, **kwargs):
    instance.roadmap.save()

