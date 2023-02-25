from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Project, Problem, Category


# Create your views here.
def index(request):
    category_list = Category.objects.all()
    projects = Project.objects.all()
    problems = Problem.objects.all()

    context = {
        'category_list':category_list,
        'projects': projects,
        'problems': problems,
    }
    return render(request,'ecoplatform/index.html',context)



