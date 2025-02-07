from django.urls import path
from .views import (
    CategorySkillListView, 
    SkillUserSearchView, 
    UserDetailView, 
    AddSkillView, 
    CategorySkillView,
    SkillResourcesView,
    RemoveSkillView,
    ResourceDeleteView,
    AddChannelView,
    SearchChannelView
    
)
from . import views

urlpatterns = [
    path("", views.main, name="main"),
    path('users/<int:user_id>/', views.user_detail_view, name='user-detail'),
    path('users/<int:user_id>/skills/<int:skill_id>/resources/', views.skill_resources_view, name='skill-resources'),
    path('find-channel/', views.findChannelView, name='find-channel'),

    # API 경로
    path('api/users/<int:user_id>/', UserDetailView.as_view(), name='user-detail'),
    path('api/users/<int:user_id>/add-skill/', AddSkillView.as_view(), name='add-skill'),
    path('api/categories/', CategorySkillListView.as_view(), name='category-skill-list'),
    path('api/categories/<int:category_id>/skills/', CategorySkillView.as_view(), name='category-skills'),
    path('api/search-users/', SkillUserSearchView.as_view(), name='search-users'),
    path('api/users/<int:user_id>/skills/<int:skill_id>/resources/', SkillResourcesView.as_view(), name='skill-resources'),
    path('api/users/<int:user_id>/skills/<int:skill_id>/resources/<int:resource_id>/', ResourceDeleteView.as_view(), name='resource-delete'),
    path('api/users/<int:user_id>/remove-skill/', RemoveSkillView.as_view(), name='remove-skill'),
    path('api/add-channel/', AddChannelView.as_view(), name='add-channel'),
    path('api/search-channel/', views.SearchChannelView.as_view(), name='search-channel'),
    path('api/add-candidate/', views.addCandidateChannelView.as_view(), name='add-candidate-channel'),
]
