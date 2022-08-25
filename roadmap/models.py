from django.db import models


class JavaScript(models.Model):
    skill_name = models.CharField(max_length=50, null=False)
    child_skills = models.ForeignKey('self', on_delete=models.CASCADE)


class js_url(models.Model):
    link = models.CharField(max_length=255, null=False)
    skill = models.ForeignKey(JavaScript, on_delete=models.CASCADE)
    link_name = models.CharField(max_length=255, null=False)
