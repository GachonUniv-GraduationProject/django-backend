from django.db import models


class JavaScript(models.Model):
    skill_name = models.CharField(max_length=50, null=False)
    base = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name='child')


class js_url(models.Model):
    link = models.CharField(max_length=255, null=False)
    skill = models.ForeignKey(JavaScript, on_delete=models.CASCADE, related_name='url')
    link_name = models.CharField(max_length=255, null=False)
