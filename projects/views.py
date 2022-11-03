from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Project
from .forms import ProjectForm, ReviewForm
from django.contrib.auth.decorators import login_required
from users.utils import searchProjects
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# Create your views here.


def project(request):
    projects, search_query = searchProjects(request)
    page = request.GET.get('page')
    result = 3
    paginator = Paginator(projects, result)
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        projects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page)

    context = {'projects': projects,
               'search_query': search_query,
               'paginator': paginator}
    return render(request, 'projects/projects.html', context)


def singleProject(request, pk):
    project = Project.objects.get(id=pk)
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.project = project
            review.owner = request.user.profile
            review.save()
            project.getVoteCount
            messages.success(request, 'Your review was sucessfully submitted')
            return redirect('project', pk=project.id)
    context = {'project': project, 'form': form}
    return render(request, 'projects/single_project.html', context)


@login_required(login_url='login')
def create(request):
    profile = request.user.profile
    form = ProjectForm()
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('account')
    return render(request, 'projects/create-project.html', {'form': form})


@login_required(login_url='login')
def update(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')
    return render(request, 'projects/update-project.html', {'form': form})


@login_required(login_url='login')
def delete(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    context = {
        'project': project
    }
    if request.method == "POST":
        project.delete()
        return redirect('projects')
    return render(request, 'delete-template.html', context)
