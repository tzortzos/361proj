"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from TAScheduler.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Index.as_view(), name='index'),

    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),


    # Users resource management
    path('users/<int:user_id>/edit/', UserEdit.as_view(), name='users-edit'),
    path('users/<int:user_id>/delete/', UserDelete.as_view(), name='users-delete'),
    path('users/<int:user_id>/', UserView.as_view(), name='users-view'),
    path('users/create/', UserCreate.as_view(), name='users-create'),
    path('users/', UserDirectory.as_view(), name='users-directory'),

    # Courses resource management
    path('courses/<int:course_id>/edit/', CoursesEdit.as_view(), name='courses-edit'),
    path('courses/<int:course_id>/delete/', CoursesDelete.as_view(), name='courses-delete'),
    path('courses/<int:course_id>/', CoursesView.as_view(), name='courses-view'),
    path('courses/create/', CoursesCreate.as_view(), name='courses-create'),
    path('courses/', CoursesDirectory.as_view(), name='courses-directory'),

    # Sections resource management
    path('sections/<int:section_id>/edit/', SectionsEdit.as_view(), name='sections-edit'),
    path('sections/<int:section_id>/delete/', SectionsDelete.as_view(), name='sections-delete'),
    path('sections/<int:section_id>', SectionsView.as_view(), name='sections-view'),
    path('sections/create/', SectionsCreate.as_view(), name='sections-create'),
    path('sections/', SectionsDirectory.as_view(), name='sections-directory'),

    # Labs resource management
    path('labs/<int:lab_id>/edit/', LabsEdit.as_view(), name='labs-edit'),
    path('labs/<int:lab_id>/delete/', LabsDelete.as_view(), name='labs-delete'),
    path('labs/<int:lab_id>/', LabsView.as_view(), name='labs-view'),
    path('labs/create/', LabsCreate.as_view(), name='labs-create'),
    path('labs/', LabsDirectory.as_view(), name='labs-directory'),

    # Skills resource management
    path('skills/<int:skill_id>/delete', SkillsDelete.as_view(), name='skills-delete'),
    path('skills/create', SkillsCreate.as_view(), name='skills-create'),
    path('skills/', SkillsDirectory.as_view(), name='skills-directory'),

]
