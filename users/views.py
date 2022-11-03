from email import message
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .utils import searchProfiles
from .models import Profile, Skill, Message
from django.shortcuts import get_object_or_404


# Create your views here.


def profiles(request):

    profiles, search_query = searchProfiles(request)
    context = {
        'profiles': profiles,
        'search_query': search_query,
    }

    return render(request, 'users/profiles.html', context)


def userProfile(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="")
    context = {
        'profile': profile,
        'topSkills': topSkills,
        'otherSkills': otherSkills
    }
    return render(request, 'users/user-profile.html', context)


def loginUser(request):
    page = 'login'
    print(request.user)
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except:
            if username != "":
                messages.error(request, f'There is no current user {username}')
            else:
                messages.error(request, f'type in a username')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            print(request.user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            messages.error(request, 'Username or password is incorrect')
    context = {
        'page': page
    }
    return render(request, 'users/login_register.html', context)


def logoutUser(request):
    logout(request)
    messages.success(request, 'logged out succesfully')
    return redirect('login')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    if request.user.is_authenticated:
        return redirect('profiles')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'user was succesfully created')
            login(request, user)
            return redirect('edit-account')
        else:
            messages.error(
                request, 'An error occurred while trying to register')
    context = {'page': page, 'form': form}

    return render(request, 'users/login_register.html', context)


@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    skills = profile.skill_set.all().order_by('-description')
    projects = profile.project_set.all()
    context = {
        'profile': profile,
        'skills': skills,
        'projects': projects
    }

    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')
        else:
            messages.error('An error Occured')
    context = {
        'form': form
    }
    return render(request, 'users/profile_form.html', context)


@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()
    context = {
        'form': form,
    }
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill successfully created')
            return redirect('account')
    return render(request, 'users/create_skill.html', context)


@login_required(login_url='login')
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)
    context = {
        'form': form,
        'skill': skill
    }
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill successfully updated')
            return redirect('account')
    return render(request, 'users/update_skill.html', context)


@login_required(login_url='login')
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    context = {
        'skill': skill
    }
    if request.method == 'POST':
        skill.delete()
    return render(request, 'delete-template.html', context)


@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messagesRequest = profile.messages.all()
    unreadCount = messagesRequest.filter(isread=False).count()
    context = {'messagesRequest': messagesRequest,
               'unreadCount': unreadCount}
    return render(request, 'users/inbox.html', context)


@login_required(login_url='login')
def viewMessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.isread == False:
        message.isread = True
        message.save()
    context = {'message': message}
    return render(request, 'users/message.html', context)


def createMessage(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)

        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient
            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()

            messages.success(request, 'Your message was sent sucessfully')

            return redirect('user-profile', pk=recipient.id)

    context = {'recipient': recipient,
               'form': form}

    return render(request, 'users/message_form.html', context)
