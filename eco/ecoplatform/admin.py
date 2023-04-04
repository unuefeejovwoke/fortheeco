from django.contrib import admin

# Register your models here.
from .models import Problem, Project, Category, Comment

admin.site.register(Problem)
admin.site.register(Project)
admin.site.register(Category)
admin.site.register(Comment)
