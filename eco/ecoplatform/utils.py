from .models import Problem
from django.shortcuts import redirect


def create_problem(user, category, location, title, description, first, second, third, last):
    print("hello")
    problem = Problem.objects.create(
        user = user,
        location= location,
        title = title,
        description = description,
        problem_photo_main = first,
        problem_photo_1 = second,
        problem_photo_2 = third,
        problem_photo_3 = last,
        category = category

    )
