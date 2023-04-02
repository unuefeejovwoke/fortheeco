from django.urls import path
from . import views

app_name = 'ecoplatform'

urlpatterns = [
    path('project/', views.projectListView, name='project_list'),
    path('problem/', views.problemListView, name='problem_list'),
    path('problem/<slug:category_slug>/', views.problemListView, name='problem_list_category'),
    path('problem/upvote/', views.upvote, name='upvote'),
    path('problem/downvote/', views.downvote, name='downvote'),

    path('project/<slug:category_slug>/', views.projectListView, name='project_list_category'),
    path('problem-detail/<str:pk>/', views.problem_detail, name='problem-detail'),
    path('project/<pk>/', views.projectDetailView, name='project_detail'),
    
    path('', views.index, name='home'),
    path('search/', views.search, name="search"),

     # load
    path('upvotes/<str:pk>/', views.upvotes, name="upvotes"),
    path('downvotes/<str:pk>/', views.downvotes, name="downvotes"),
    path('upvotes_count/<str:pk>/', views.upvotes_count, name="upvotes_count"),
    path('downvotes_count/<str:pk>/', views.downvotes_count, name="downvotes_count")

   
]
