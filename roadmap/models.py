from django.db import models


class skills(models.Model):
    name = models.CharField(max_length=100, null=False)
    base = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name='child')
    field = models.CharField(max_length=50, null=False)

    def __str__(self):
        return "id:"+str(self.id)+" name:"+self.name+" field:"+self.field+" base: "+str(self.base)


class url(models.Model):
    link = models.CharField(max_length=255, null=False)
    skill = models.ForeignKey(skills, on_delete=models.CASCADE, related_name='url')
    link_name = models.CharField(max_length=255, null=False)
