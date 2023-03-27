from django.urls import path
from . import views

app_name = 'ecoplatform'

urlpatterns = [
    path('project/', views.projectListView, name='project_list'),
    path('problem/', views.problemListView, name='problem_list'),
    path('problem/<slug:category_slug>/', views.problemListView, name='problem_list_category'),
    path("upvote_problem", views.upvote_problem, name="upvote"),
    
    path('project/<slug:category_slug>/', views.projectListView, name='project_list_category'),
    path('problem/<pk>/', views.problemDetailView, name='problem_detail'),
    path('project/<pk>/', views.projectDetailView, name='project_detail'),
    
    path('', views.index, name='home'),
    path('search/', views.search, name="search"),
]
