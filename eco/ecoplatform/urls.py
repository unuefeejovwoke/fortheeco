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
    path('problem/add_comment_to_problem/<int:pk>/', views.add_comment, name='add_comment_to_problem'),
    path('comment/<int:pk>/like/', views.like_comment, name='like-comment'),
    path('comment/<int:pk>/dislike/', views.dislike_comment, name='dislike-comment'),

    path('project/<pk>/', views.projectDetailView, name='project_detail'),
    
    path('', views.index, name='home'),
    path('search/', views.search, name="search"),

     # load
    path('upvotes/<str:pk>/', views.upvotes, name="upvotes"),
    path('downvotes/<str:pk>/', views.downvotes, name="downvotes"),
    path('upvotes_count/<str:pk>/', views.upvotes_count, name="upvotes_count"),
    path('downvotes_count/<str:pk>/', views.downvotes_count, name="downvotes_count"),


    # add problem
    path('add-problem/', views.add_problem, name="add-problem"),
    path('display/', views.form_display, name="display")

   
]
