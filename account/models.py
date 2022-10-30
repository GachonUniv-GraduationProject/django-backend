# api/models.py
from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_pk = models.IntegerField(blank=True)
    email = models.EmailField(max_length=500, blank=True)
    nickname = models.CharField(max_length=200, blank=True)
    point = models.IntegerField(default=0)
    like = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=200, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, user_pk=instance.id)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
#
#
#
#
#
# # class tech_stack(models.Model):
# #     name = models.CharField(max_length=100, null=False, blank=False)
#
#
# class UserManager(BaseUserManager):
#     # 일반 user 생성
#     def create_user(self, email, nickname, name, password=None):
#         if not email:
#             raise ValueError('must have user email')
#         if not nickname:
#             raise ValueError('must have user nickname')
#         if not name:
#             raise ValueError('must have user name')
#         user = self.model(
#             email=self.normalize_email(email),
#             nickname=nickname,
#             name=name
#         )
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     # 관리자 user 생성
#     def create_superuser(self, email, nickname, name, password=None):
#         user = self.create_user(
#             email,
#             password=password,
#             nickname=nickname,
#             name=name
#         )
#         user.is_admin = True
#         user.save(using=self._db)
#         return user
#
#
# class User(AbstractBaseUser):
#     id = models.AutoField(primary_key=True)
#     email = models.EmailField(default='', max_length=100, null=False, blank=False, unique=True)
#     nickname = models.CharField(default='', max_length=100, null=False, blank=False, unique=True)
#     name = models.CharField(default='', max_length=100, null=False, blank=False)
#     # tech_stacks = models.ManyToManyField(tech_stack, default=None)
#
#     # User 모델의 필수 field
#     is_active = models.BooleanField(default=True)
#     is_admin = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)
#
#     # 헬퍼 클래스 사용
#     objects = UserManager()
#
#     # 사용자의 username field는 nickname으로 설정
#     USERNAME_FIELD = 'nickname'
#     # 필수로 작성해야하는 field
#     REQUIRED_FIELDS = ['email', 'name']
#
#     def __str__(self):
#         return self.nickname
#
#     def info(self):
#         return str(self.id)+" "+str(self.email)+" "+str(self.nickname)
#
#     def has_perm(self, perm, obj=None):
#         return True
#
#     def has_module_perms(self, app_label):
#         return True
#
#     @property
#     def is_staff(self):
#         return self.is_admin
