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

#message notif import
from django.contrib import messages

#for chart
import json

from django.db.models import Count
from .models import Student,Program, College, Organization, OrgMember
from django.db.models.functions import TruncYear

"""
def chart_view(request):
    # College chart
    colleges = College.objects.annotate(total=Count('program__student')).order_by('college_name')
    college_names = [college.college_name for college in colleges]
    student_counts = [college.total for college in colleges]

    # Program chart
    programs = Program.objects.annotate(student_count=Count('student')).order_by('-student_count')
    program_names = [program.prog_name for program in programs]
    program_counts = [program.student_count for program in programs]

    # Students per Organization chart (new)
    organizations = Organization.objects.annotate(student_count=Count('orgmember')).order_by('name')
    org_names = [org.name for org in organizations]
    org_student_counts = [org.student_count for org in organizations]

    context = {
        'college_names': json.dumps(college_names),
        'student_counts': json.dumps(student_counts),
        'program_names': json.dumps(program_names),
        'program_counts': json.dumps(program_counts),
        'org_names': json.dumps(org_names),
        'org_student_counts': json.dumps(org_student_counts),
    }

    return render(request, 'chart.html', context)
"""

from django.db.models import Count
import json

def chart_view(request):
    # College chart: Number of students per college
    colleges = College.objects.annotate(total=Count('program__student')).order_by('college_name')
    college_names = [college.college_name for college in colleges]
    student_counts = [college.total for college in colleges]

    # Program chart: Top programs by number of students
    programs = Program.objects.annotate(student_count=Count('student')).order_by('-student_count')
    program_names = [program.prog_name for program in programs]
    program_counts = [program.student_count for program in programs]

    # Top 5 Organizations by Number of Student Members (Bar Chart)
    top_organizations = Organization.objects.annotate(student_count=Count('orgmember')).order_by('-student_count')[:5]
    org_names = [org.name for org in top_organizations]
    org_student_counts = [org.student_count for org in top_organizations]

    # Student Enrollment Over Time chart (by year)
    student_enrollment_by_year = Student.objects.annotate(
        year=TruncYear('created_at')
    ).values('year').annotate(
        total=Count('id')
    ).order_by('year')

    college_years = [entry['year'].year for entry in student_enrollment_by_year]
    counts_by_year = [entry['total'] for entry in student_enrollment_by_year]

    context = {
        'college_names': json.dumps(college_names),
        'student_counts': json.dumps(student_counts),
        'program_names': json.dumps(program_names),
        'program_counts': json.dumps(program_counts),
        'org_names': json.dumps(org_names),
        'org_student_counts': json.dumps(org_student_counts),
        'college_years': json.dumps(college_years),
        'counts_by_year': json.dumps(counts_by_year),
    }

    return render(request, 'chart.html', context)



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

    def form_valid(self, form):
        name = form.cleaned_data['name']
        messages.success(self.request, f" '{name} organization created successfully.'")   
        return super().form_valid(form)

    

class OrganizationUpdateView(UpdateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'org_edit.html'
    success_url = reverse_lazy('organization-list')

    def form_valid(self, form):
        name = form.cleaned_data['name']
        messages.success(self.request, f" '{name} organization updated successfully.'")   
        return super().form_valid(form)

class OrganizationDeleteView(DeleteView):
    model = Organization
    template_name = 'org_del.html'
    success_url = reverse_lazy('organization-list')

    def form_valid(self, form):
        name = self.object.name
        messages.success(self.request, f"' {name}' organization deleted successfully.")   
        return super().form_valid(form)

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

    def form_valid(self, form):
        student = form.cleaned_data['student']
        organization = form.cleaned_data['organization']
        messages.success(self.request, f" '{student} added successfully in {organization} organization.'")   
        return super().form_valid(form)


class OrgMembersUpdateView(UpdateView):
    model = OrgMember
    form_class = OrgMembersForm
    template_name = 'org_members_edit.html'
    success_url = reverse_lazy('org-members-list')

    def form_valid(self, form):
        student = form.cleaned_data['student']
        organization = form.cleaned_data['organization']
        messages.success(self.request, f" '{student} updated transfer organization to {organization} successfully.'")   
        return super().form_valid(form)


class OrgMembersDeleteView(DeleteView):
    model = OrgMember
    template_name = 'org_members_del.html'
    success_url = reverse_lazy('org-members-list')

    def form_valid(self, form):
        student = self.object.student 
        organization = getattr(self.object, 'organization', None)
        messages.success(self.request, f"' {student}' deleted successfully from {organization} organization.")   
        return super().form_valid(form)

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

    def form_valid(self, form):
        student = form.save()
        messages.success(self.request, f"Student '{student.student_id}' was added successfully.")
        return super().form_valid(form)



class StudentsUpdateView(UpdateView):
    model = Student
    form_class = StudentsForm
    template_name = 'students_edit.html'
    success_url = reverse_lazy('students-list')
    
    def form_valid(self, form):
        student = form.save(commit=False)  # get the instance without saving to DB yet
        messages.success(self.request, f"'{student.student_id}' updated successfully.")
        return super().form_valid(form)


class StudentsDeleteView(DeleteView):
    model = Student
    template_name = 'students_del.html'
    success_url = reverse_lazy('students-list')

    def form_valid(self, form):
        student_id = self.object.student_id 
        messages.success(self.request, f"'{student_id}' deleted successfully.")   
        return super().form_valid(form)



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

    def form_valid(self, form):
        college_name = form.cleaned_data['college_name']
        messages.success(self.request, f" '{college_name} added successfully.'")   
        return super().form_valid(form)


class CollegesUpdateView(UpdateView):
    model = College
    form_class = CollegesForm
    template_name = 'college_edit.html'
    success_url = reverse_lazy('college-list')

    def form_valid(self, form):
        college_name = form.cleaned_data['college_name']
        messages.success(self.request, f" '{college_name} updated successfully.'")   
        return super().form_valid(form)
    

class CollegesDeleteView(DeleteView):
    model = College
    template_name = 'college_del.html'
    success_url = reverse_lazy('college-list')

    def form_valid(self, form):
        college_name = self.object.college_name 
        messages.success(self.request, f"'{college_name}' deleted successfully.")   
        return super().form_valid(form)


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

    def form_valid(self, form):
        prog_name = form.cleaned_data['prog_name']
        messages.success(self.request, f" '{prog_name} program added successfully.'")   
        return super().form_valid(form)


class ProgramsUpdateView(UpdateView):
    model = Program
    form_class = ProgramsForm
    template_name = 'program_edit.html'
    success_url = reverse_lazy('program-list')

    def form_valid(self, form):
        prog_name = form.cleaned_data['prog_name']
        messages.success(self.request, f" '{prog_name} program updated successfully.'")   
        return super().form_valid(form)
   

class ProgramsDeleteView(DeleteView):
    model = Program
    template_name = 'program_del.html'
    success_url = reverse_lazy('program-list')

    def form_valid(self, form):
        prog_name = self.object.prog_name
        messages.success(self.request, f"' {prog_name}' program deleted successfully.")   
        return super().form_valid(form)



       