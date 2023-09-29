from django.db.models import Q
from projects.models import Project
from .models import Profile, Skill


def searchProfiles(request):
    search_query = ""
    if request.GET.get("search_query"):
        search_query = request.GET.get("search_query")
        print(search_query)

    skills = Skill.objects.filter(name__icontains=search_query)
    profiles = Profile.objects.distinct().filter(
        Q(username__icontains=search_query)
        | Q(short_intro__icontains=search_query)
        | Q(skill__in=skills)
    )
    return profiles, search_query


def searchProjects(request):
    search_query = ""
    if request.GET.get("project_search_query"):
        search_query = request.GET.get("project_search_query")
    profiles = Profile.objects.filter(name__icontains=search_query)
    projects = Project.objects.filter(
        Q(title__icontains=search_query) | Q(owner__in=profiles)
    )

    return projects, search_query
