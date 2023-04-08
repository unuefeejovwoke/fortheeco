from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Project, Problem, Category, Comment
from django.contrib import messages, auth

from .forms import CommentForm
from django.db.models import Q
from .filters import ProblemFilter, ProjectFilter
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import json
from .utils import create_problem


# Create your views here.

def index(request):
    # Create a context dictionary with the data you want to pass to the template
    category_list = Category.objects.all()

    # Get all the problems from the database
    problems = Problem.objects.all()

    # Loop through each problem to get its associated comments count
    comments = {}
    for problem in problems:
        comments[problem.id] = problem.comments.count()

    total_problems = problems.count()
    total_projects = Project.objects.all().count()
    projects = Project.objects.all()

    context = {
        'category_list': category_list,
        'total_problems': total_problems,
        'total_projects': total_projects,
        'projects': projects,
        'problems': problems,
        'home': 'home',
        'comments': comments,
    }

    # Render the template with the context dictionary and return the rendered HTML
    return render(request, 'ecoplatform/index.html', context)





#list view for the problems
# list view for the problems
def problemListView(request, category_slug=None):
    category_slug = request.GET.get('category')
    user_query = request.GET.get('user_query')
    location_query = request.GET.get('location_query')
    
    # Filter by category
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        problems = Problem.objects.filter(category=category)
    else:
        category = None
        problems = Problem.objects.all()

    comments = {}
    for problem in problems:
        comments[problem.id] = problem.comments.count()

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
        'comments':comments,
    }
    return render(request, 'ecoplatform/problem_list.html', context)



#detail view for the problem
def problem_detail(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    comments = problem.comments.all()


    context = {
        'problem': problem,
        'comments': comments,
    }
    return render(request, 'ecoplatform/problem_detail.html', context)

@login_required(login_url="ecousers:login")
def add_comment(request, pk):
    problem = get_object_or_404(Problem, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user  # Set the user field to the currently logged-in user
            comment.problem = problem
            comment.save()
            messages.success(request, 'Your comment was made successfully')
            return redirect('ecoplatform:problem-detail', pk=problem.pk)
    else:
        form = CommentForm()

    return render(request, 'ecoplatform/add_comment_to_problem.html', {'form': form})

@login_required(login_url="ecousers:login")
def like_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    user = request.user

    if user in comment.dislikes.all():
        comment.dislikes.remove(user)
        comment.likes.add(user)
    elif user in comment.likes.all():
        comment.likes.remove(user)
    else:
        comment.likes.add(user)

    likes_count = comment.likes.count()
    dislikes_count = comment.dislikes.count()
    response_data = {'likes_count': likes_count, 'dislikes_count': dislikes_count}

    return JsonResponse(response_data)


@login_required(login_url="ecousers:login")
def dislike_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    user = request.user

    if user in comment.likes.all():
        comment.likes.remove(user)
        comment.dislikes.add(user)
    elif user in comment.dislikes.all():
        comment.dislikes.remove(user)
    else:
        comment.dislikes.add(user)

    likes_count = comment.likes.count()
    dislikes_count = comment.dislikes.count()
    response_data = {'likes_count': likes_count, 'dislikes_count': dislikes_count}

    return JsonResponse(response_data)

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
        projects = Project.objects.order_by('-created').filter(category=category)
    else:
        projects = Project.objects.order_by('-created').all()

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
   
    


    # forms

@login_required(login_url="ecousers:login")
def add_problem(request):
    if request.method == "POST":
        user = request.user
        location = request.POST.get("location")
        description = request.POST.get("description")
        first = request.FILES.get("first_image")
        second = request.FILES.get("second_image")
        third = request.FILES.get("third_image")
        last = request.FILES.get("last_image")
        category = request.POST.get("category")
        category = Category.objects.get(name = category.capitalize())
        # print(category)
        # print(first)
        #  environment
        title = request.POST.get("title")
        title = title.replace("_", " ")
        # print(title)
        create_problem(user, category, location, title, description, first, second, third, last)
        messages.success(request, "Problem add successfully")
        return redirect("ecoplatform:problem_list")

    return render(request, "ecoplatform/add-problem.html")



@login_required(login_url="ecousers:login")
def add_project(request):
    if request.method == "POST":
        location = request.POST.get("location")
        category = request.POST.get("category")
        title = request.POST.get("title")
        sponsor = request.POST.get("sponsor-name")
        description = request.POST.get("description")
        linkedin = request.POST.get("linkedin")
        twitter = request.POST.get("twitter")
        instagram = request.POST.get("instagram")
        Gmail = request.POST.get("Gmail")
        category = Category.objects.get(name = category.capitalize())
        title = request.POST.get("title")
        title = title.replace("_", " ")

        Project.objects.create(
            user = request.user,
            title = title,
            location = location,
            description = description,
            sponsor = sponsor,
            category = category,
            linkedin = linkedin,
            twitter = twitter,
            instagram = instagram,
            Gmail = Gmail
        )
        messages.success(request, "project added successfully")
        return redirect("ecoplatform:project_list")


    return render(request, "ecoplatform/add-project.html")

def form_display(request):
    name=request.GET.get("category")
    print(name)
    context = {
        "name" : name
    }
    return render(request, "ecoplatform/display.html", context)