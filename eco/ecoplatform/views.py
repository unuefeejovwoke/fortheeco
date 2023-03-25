from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Project, Problem, Category
from django.db.models import Q
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

#list view for the problems
def problemListView(request):
    category_slug = request.GET.get('category')
    user_query = request.GET.get('user_query')
    location_query = request.GET.get('location_query')

    # Filter by category
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        problems = Problem.objects.filter(category=category)
    else:
        problems = Problem.objects.all()

    # Filter by user query
    if user_query:
        problems = problems.filter(description__icontains=user_query)

    # Filter by location query
    if location_query:
        problems = problems.filter(location__icontains=location_query)

    categories = Category.objects.all()

    context = {
        'problems': problems,
        'categories': categories,
        'selected_category': category_slug,
    }
    return render(request, 'ecoplatform/problem_list.html', context)

def search(request):
    category_list = Category.objects.annotate(total_problems=Count('problem'))
    context = {'category_list': category_list}
    
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            problems = Problem.objects.filter(Q(location__icontains=keyword) | Q(description__icontains=keyword))
            problem_count = problems.count()
            context.update({
                'problems': problems,
                'problem_count':  problem_count,
                'keyword':keyword,
            })
    return render(request, 'ecoplatform/problem_list.html', context)

#detail view for the problem
def problemDetailView(request, pk):
    context = {'problem_detail': Problem.objects.get(pk=pk)}
    return render(request, 'ecoplatform/problem_detail.html', context)

#list view for the projects
def projectListView(request):
    category_slug = request.GET.get('category')
    user_query = request.GET.get('user_query')
    location_query = request.GET.get('location_query')

    # Filter by category
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        projects = Project.objects.filter(category=category)
    else:
        projects = Project.objects.all()

    # Filter by user query
    if user_query:
        projects = projects.filter(description__icontains=user_query)

    # Filter by location query
    if location_query:
        projects = projects.filter(location__icontains=location_query)

    categories = Category.objects.all()

    context = {
        'projects': projects,
        'categories': categories,
        'selected_category': category_slug,
    }
    return render(request, 'ecoplatform/project_list.html', context)



#detail view for the project
def projectDetailView(request, pk):
    context = {'project_detail': Project.objects.get(pk=pk)}
    return render(request, 'ecoplatform/project_detail.html', context)