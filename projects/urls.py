from django.urls import path
from . import views
urlpatterns = [
    path('', views.project, name='projects'),
    path('project/<str:pk>/', views.singleProject, name='project'),
    path('create-project/', views.create, name='create-project'),
    path('update-project/<str:pk>/', views.update, name='update-project'),
    path('delete/<str:pk>/', views.delete, name='delete-project')
]
