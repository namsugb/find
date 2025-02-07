from django.contrib import admin
from .models import Category, Skill, User, Material
from scraper.models import Channel, candidate
from django.contrib.auth.admin import UserAdmin


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']    


@admin.register(Skill)
class skillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']    


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + (
        ("feature", {"fields": ("skills","bio", "profile_picture")}),
    )
    list_display = ("username", "email", "is_staff", "is_active", "get_skills")

    def get_skills(self, obj):
        return ", ".join([skill.name for skill in obj.skills.all()])
    get_skills.short_description = "Skills"    


@admin.register(Material)    
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'skill']


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ['channel_id', 'title']

@admin.register(candidate)
class candidateChannelAdmin(admin.ModelAdmin):
    list_display = ['channel_id']    