from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Project, Problem, Category
from .filters import ProblemFilter, ProjectFilter
# Create your views here.

def index(request):
    category_list = Category.objects.all()
    problem_filter = ProblemFilter(request.GET, queryset=Problem.objects.all())
    project_filter = ProjectFilter(request.GET, queryset=Project.objects.all())
    projects = Project.objects.all()
    problems = Problem.objects.all()

    context = {
        'category_list':category_list,
        'problems': problem_filter,
        'projects': project_filter,
    }
    return render(request,'ecoplatform/index.html',context)
