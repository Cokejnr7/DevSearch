

# def searchProjects(request):
#     search_query = ''
#     if request.GET.get('project_search_query'):
#         search_query = request.GET.get('project_search_query')
#     profiles = Profile.objects.filter(name__icontains=search_query)
#     projects = Project.objects.filter(
#         Q(title__icontains=search_query) | Q(owner__in=profiles))

#     return projects, search_query
