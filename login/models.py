from django.db import models


# Create your models here.
class User(models.Model):
    user_name = models.TextField(max_length=25)
    phone = models.TextField()
    address = models.TextField()
    email = models.TextField(unique=True)
    nickname = models.TextField(max_length=25, unique=True)

    class Meta:
        db_table = "user"



