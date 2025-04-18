"""
URL configuration for projectsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, re_path
from studentorg.views import HomePageView, OrganizationList, OrganizationCreateView, OrganizationUpdateView, OrganizationDeleteView
from studentorg.views import OrgMembersList, OrgMembersCreateView, OrgMembersUpdateView, OrgMembersDeleteView
from studentorg.views import StudentsList, StudentsCreateView, StudentsUpdateView, StudentsDeleteView
from studentorg.views import CollegesList, CollegesCreateView, CollegesUpdateView, CollegesDeleteView
from studentorg.views import ProgramList, ProgramsCreateView, ProgramsUpdateView, ProgramsDeleteView
from studentorg import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomePageView.as_view(), name='home'),

    #Login and Logout URLs
    
    re_path(r'^accounts/login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    re_path(r'^accounts/logout/$', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),

    # Organization URLs

    path('organization_list', OrganizationList.as_view(), name='organization-list'),
    path('organization_list/add', OrganizationCreateView.as_view(), name='organization-add'),
    path('organization_list/<pk>', OrganizationUpdateView.as_view(), name='organization-update'),
    path('organization_list/<pk>/delete', OrganizationDeleteView.as_view(), name='organization-delete'),

    # Org Member URLs
    
    path('org_members_list', OrgMembersList.as_view(), name='org-members-list'),
    path('org_members_list/add', OrgMembersCreateView.as_view(), name='org-members-add'),
    path('org_members_list/<pk>', OrgMembersUpdateView.as_view(), name='org-members-update'),
    path('org_members_list/<pk>/delete', OrgMembersDeleteView.as_view(), name='org-member-delete'),

    # Students URLs

    path('students_list', StudentsList.as_view(), name='students-list'),
    path('students_list/add', views.StudentsCreateView.as_view(), name='students-add'),
    path('students_list/<pk>', views.StudentsUpdateView.as_view(), name='students-update'),
    path('students_list/<pk>/delete', views.StudentsDeleteView.as_view(), name='students-delete'),

    # College URls

    path('college_list', CollegesList.as_view(), name='college-list'),
    path('college_list/add', CollegesCreateView.as_view(), name='college-add'),
    path('college_list/<pk>', CollegesUpdateView.as_view(), name='college-update'),
    path('college_list/<pk>/delete', CollegesDeleteView.as_view(), name='college-delete'),
    
    # Program URLs
    path('program_list', ProgramList.as_view(), name='program-list'),
    path('program_list/add', ProgramsCreateView.as_view(), name='program-add'),
    path('program_list/<pk>', ProgramsUpdateView.as_view(), name='program-update'),
    path('program_list/<pk>/delete', ProgramsDeleteView.as_view(), name='program-delete'),
]
