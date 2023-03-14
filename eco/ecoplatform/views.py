from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Project, Problem, Category
from .filters import ProblemFilter, ProjectFilter
from django.db.models import Count
from django.shortcuts import get_object_or_404

# Create your views here.

def index(request):
    category_list = Category.objects.all()
    total_problems = Problem.objects.all().count()
    total_projects = Project.objects.all().count()
    projects = Project.objects.all()
    problems = Problem.objects.all()

    context = {
        'category_list':category_list,
        'total_problems': total_problems,
        'total_projects': total_projects,
    }
    return render(request,'ecoplatform/index.html',context)

#list view for the problems
def problemListView(request, category_slug=None):
    category = None
    problem_list = Problem.objects.all()
    category_list = Category.objects.annotate(total_problems=Count('problem'))
    selected_category_slug = 'All'  # default to "All" category
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        problem_list = problem_list.filter(category=category)
        selected_category_slug = category_slug
    
    context = {
        'problem_list': problem_list,
        'category_list': category_list,
        'category': category,
        'selected_category_slug': selected_category_slug,  # pass selected category slug to template
    }
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