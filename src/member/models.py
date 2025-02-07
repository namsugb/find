from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    skills = models.ManyToManyField(
        'Skill',
        related_name='users',
        blank=True,
        help_text=_("사용자가 보유한 기술 목록"),
    )
    bio = models.TextField(blank=True, help_text=_("사용자의 자기 소개"))
    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        blank=True,
        null=True,
        help_text=_("사용자 프로필 사진"),
    )

    # 'groups'와 'user_permissions'의 related_name 변경
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_groups",
        blank=True,
        help_text=_("사용자가 속한 그룹"),
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions",
        blank=True,
        help_text=_("사용자에 부여된 권한"),
    )

    def __str__(self):
        return self.username

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name
    
class Skill(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='skills')

    def __str__(self):
        return self.name
    
class Material(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='materials')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='materials', null=True)
    title = models.CharField(max_length=200)
    link = models.URLField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title    
     
