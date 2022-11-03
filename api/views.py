from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from projects.models import Project, Review
from .serializers import ProjectSerializer, ReviewSerializer
# Create your views here.


@api_view(['GET'])
def getRoutes(request):
    routes = [
        {'GET': 'api/projects'},
        {'GET': 'api/projects/id'},
        {'POST': 'api/projects/id/vote'},
        {'POST': 'api/users/token'},
        {'POST': 'api/users/token/refresh'},
    ]
    return Response(routes)


@api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
def getProjects(request):
    if request.method == 'GET':
        print(request.user)
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        data = {
            "message": "success",
            "data": serializer.data
        }

        return Response(data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = ProjectSerializer(data=request.data, many=False)
        if serializer.is_valid():
            serializer.save()
            data = {
                "message": "success",
                "data": serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = {
                "message": "failed",
                "error": serializer.errors
            }

            return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getProject(request, pk):
    projects = Project.objects.get(id=pk)
    serializer = ProjectSerializer(projects, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def projectVotes(request, pk):
    project = Project.objects.get(id=pk)
    user = request.user.profile
    data = request.data
    review, created = Review.objects.get_or_create(owner=user, project=project)
    review.value = data['value']
    review.save()
    project.getVoteCount
    serializer = ProjectSerializer(project, many=False)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
