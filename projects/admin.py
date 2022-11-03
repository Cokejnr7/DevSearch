from dataclasses import fields
from django.contrib import admin
from .models import Project, Tag, Review
# Register your models here.


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    model = Project
    field = '__all__'


@admin.register(Review)
class ProjectAdmin(admin.ModelAdmin):
    model = Review
    field = '__all__'


@admin.register(Tag)
class ProjectAdmin(admin.ModelAdmin):
    model = Tag
    field = '__all__'
