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

#list view for the problems
def problemListView(request):
    problems = Problem.objects.all()
    problem_filter = ProblemFilter(request.GET, queryset=problems)
    context = {'problems': problem_filter}
    return render(request, 'ecoplatform/problem_list.html', context)

#detail view for the problem
def problemDetailView(request, pk):
    context = {'problem_detail': Problem.objects.get(pk=pk)}
    return render(request, 'ecoplatform/problem_detail.html', context)

#list view for the projects
def projectListView(request):
    projects = Project.objects.all()
    project_filter = ProblemFilter(request.GET, queryset=projects)
    context = {'projects': project_filter}
    return render(request, 'ecoplatform/project_list.html', context)

#detail view for the project
def projectDetailView(request, pk):
    context = {'project_detail': Project.objects.get(pk=pk)}
    return render(request, 'ecoplatform/project_detail.html', context)