from django.urls import path
from .views import index, problemListView, problemDetailView, projectListView, projectDetailView

app_name = 'ecoplatform'


urlpatterns = [
    path('project/', projectListView, name='project_list'),
    path('problem/', problemListView, name='problem_list'),
    path('problem/<id>/', problemDetailView, name='problem_detail'),
    path('project/<id>/', projectDetailView, name='project_detail'),
    path('', index, name='index'),
]