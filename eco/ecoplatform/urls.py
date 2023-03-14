from django.urls import path
from . import views

app_name = 'ecoplatform'


urlpatterns = [
    path('project/', views.projectListView, name='project_list'),
    path('problem/', views.problemListView, name='problem_list'),
    path('problem/<slug:category_slug>/', views.problemListView, name='problem_list_category'),

    path('problem/<pk>/', views.problemDetailView, name='problem_detail'),
    path('project/<pk>/', views.projectDetailView, name='project_detail'),
    path('', views.index, name='home'),
]