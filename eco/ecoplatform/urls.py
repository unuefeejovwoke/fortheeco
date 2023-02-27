from django.urls import path
from . import views

app_name = 'ecoplatform'

urlpatterns = [
    path('', views.index, name='home'),
]