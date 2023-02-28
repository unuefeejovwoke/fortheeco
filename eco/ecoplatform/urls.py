from django.urls import path
from .views import index, problemDetailView, projectDetailView

app_name = 'ecoplatform'

urlpatterns = [
    path('problem/<id>/', problemDetailView, name='problem_detail'),
    path('project/<id>/', projectDetailView, name='project_detail'),
    path('', index, name='index'),
]