# api/models.py
from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# member profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_pk = models.IntegerField(blank=True)
    display_name = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=200, blank=True)
    is_individual = models.BooleanField(default=True)
    open_to_company = models.BooleanField(default=True)

# member experience
class Experience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_pk = models.IntegerField(default=0)
    field = models.CharField(max_length=200)
    detail = models.CharField(max_length=500)

# field
class Field(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_pk = models.IntegerField(default=0)
    name = models.CharField(max_length=200, blank=True, null=True)
    preference = models.IntegerField(blank=True, null=True)

# roadmap
class Roadmap(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_pk = models.IntegerField(blank=True, default=-1)
    field_name = models.CharField(max_length=200, blank=True, null=True)
    progress = models.CharField(max_length=200, blank=True, null=True)

# company
class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_pk = models.IntegerField(blank=True, default=-1)
    company_name = models.CharField(max_length=200, blank=True)

# recommended profile
class RecommendProfile(models.Model):
    user_pk = models.IntegerField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    match_ratio = models.FloatField()
    skills = models.CharField(max_length=1000, default="")


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
