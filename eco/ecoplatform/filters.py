from .models import Problem, Project
import django_filters

class ProblemFilter(django_filters.FilterSet):
    class Meta:
        model = Problem
        fields = ('isTrending', )

class ProjectFilter(django_filters.FilterSet):
    class Meta:
        model = Project
        fields = ('isTrending',)
