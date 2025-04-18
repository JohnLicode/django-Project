from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from studentorg.models import Organization, OrgMember, Student, College, Program
from studentorg.forms import OrganizationForm, OrgMembersForm, StudentsForm, CollegesForm, ProgramsForm
from django.urls import reverse_lazy
from typing import Any
from django.db.models.query import QuerySet
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required



# Create your views here.

# Organization List View

class HomePageView(ListView):
    model = Organization
    context_object_name = 'home'
    template_name = "home.html"

class OrganizationList(ListView):
    model = Organization
    context_object_name = 'organization'
    template_name = "org_list.html"
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        qs = super(OrganizationList, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query)
            )
        return qs
    
class OrganizationCreateView(CreateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'org_add.html'
    success_url = reverse_lazy('organization-list')

class OrganizationUpdateView(UpdateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'org_edit.html'
    success_url = reverse_lazy('organization-list')

class OrganizationDeleteView(DeleteView):
    model = Organization
    template_name = 'org_del.html'
    success_url = reverse_lazy('organization-list')

# Org Member List View

class OrgMembersList(ListView):
    model = OrgMember
    context_object_name = 'org_member'
    template_name = "org_members_list.html"
    paginate_by = 5

class OrgMembersCreateView(CreateView):
    model = OrgMember
    form_class = OrgMembersForm
    template_name = 'org_members_add.html'
    success_url = reverse_lazy('org-members-list')

class OrgMembersUpdateView(UpdateView):
    model = OrgMember
    form_class = OrgMembersForm
    template_name = 'org_members_edit.html'
    success_url = reverse_lazy('org-members-list')

class OrgMembersDeleteView(DeleteView):
    model = OrgMember
    template_name = 'org_members_del.html'
    success_url = reverse_lazy('org-members-list')

# Students List View

class StudentsList(ListView):
    model = Student
    context_object_name = 'students'
    template_name = "students_list.html"
    paginate_by = 5


class StudentsCreateView(CreateView):
    model = Student
    form_class = StudentsForm
    template_name = 'students_add.html'
    success_url = reverse_lazy('students-list')


class StudentsUpdateView(UpdateView):
    model = Student
    form_class = StudentsForm
    template_name = 'students_edit.html'
    success_url = reverse_lazy('students-list')


class StudentsDeleteView(DeleteView):
    model = Student
    template_name = 'students_del.html'
    success_url = reverse_lazy('students-list') 

# College List View

class CollegesList(ListView):
    model = College
    context_object_name = 'colleges'
    template_name = "college_list.html"
    paginate_by = 5
    ordering = ['college_name']    #adding ordering variable to fix the issue of ordering in the college list view
    
class CollegesCreateView(CreateView):
    model = College
    form_class = CollegesForm
    template_name = 'college_add.html'
    success_url = reverse_lazy('college-list')


class CollegesUpdateView(UpdateView):
    model = College
    form_class = CollegesForm
    template_name = 'college_edit.html'
    success_url = reverse_lazy('college-list')

class CollegesDeleteView(DeleteView):
    model = College
    template_name = 'college_del.html'
    success_url = reverse_lazy('college-list')


#Program list view

class ProgramList(ListView):
    model = Program
    context_object_name = 'programs'
    template_name = "program_list.html"
    paginate_by = 5
    
class ProgramsCreateView(CreateView):
    model = Program
    form_class = ProgramsForm
    template_name = 'program_add.html'
    success_url = reverse_lazy('program-list')


class ProgramsUpdateView(UpdateView):
    model = Program
    form_class = ProgramsForm
    template_name = 'program_edit.html'
    success_url = reverse_lazy('program-list')
   

class ProgramsDeleteView(DeleteView):
    model = Program
    template_name = 'program_del.html'
    success_url = reverse_lazy('program-list')