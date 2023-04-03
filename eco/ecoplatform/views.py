from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Project, Problem, Category
from django.db.models import Q
from .filters import ProblemFilter, ProjectFilter
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import json


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
        "home":"home"
    }
    return render(request,'ecoplatform/index.html',context)

#list view for the problems

#list view for the problems
# list view for the problems
def problemListView(request, category_slug=None):
    user_query = request.GET.get('user_query')
    location_query = request.GET.get('location_query')

    # Filter by category
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        problems = Problem.objects.filter(category=category)
    else:
        category = None
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
        'category': category,
       
    }
    return render(request, 'ecoplatform/problem_list.html', context)


#detail view for the problem
def problem_detail(request, pk):
    context = {'problem': Problem.objects.get(pk=pk)}
    return render(request, 'ecoplatform/problem_detail.html', context )




@require_POST
def upvote(request):
    problem_id = request.POST.get('problem_id')
    category_id = request.POST.get('category_id')
    if problem_id:
        problem = get_object_or_404(Problem, id=problem_id)
        problem.upvote()
        if category_id:
            category = get_object_or_404(Category, id=category_id)
            category.upvote()
        return JsonResponse({'success': True, 'votes': problem.votes})
    else:
        return JsonResponse({'success': False})


@require_POST
def downvote(request):
    problem_id = request.POST.get('problem_id')
    category_id = request.POST.get('category_id')
    if problem_id:
        problem = get_object_or_404(Problem, id=problem_id)
        problem.downvote()
        if category_id:
            category = get_object_or_404(Category, id=category_id)
            category.downvote()
        return JsonResponse({'success': True, 'votes': problem.votes})
    else:
        return JsonResponse({'success': False})

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



def upvotes(request, pk):
    problem = Problem.objects.get(id=pk)
    problem.downvotes.remove(request.user)
    problem.upvotes.add(request.user)


def upvotes_count(request, pk):
    problem = Problem.objects.get(id=pk)
    return render(request, "load/upvote.html", {"problem":problem})


def downvotes(request, pk):
    problem = Problem.objects.get(id=pk)
    problem.upvotes.remove(request.user)
    problem.downvotes.add(request.user)

def downvotes_count(request, pk):
    problem = Problem.objects.get(id=pk)
    return render(request, "load/downvote.html", {"problem":problem})
   
    