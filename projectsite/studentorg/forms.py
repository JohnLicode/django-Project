from django.forms import ModelForm
from django import forms
from .models import Organization, OrgMember, Student, College

class OrganizationForm(ModelForm):
    class Meta:
        model = Organization
        fields = "__all__"

class OrgMembersForm(ModelForm):
    class Meta:
        model = OrgMember
        fields = "__all__"

class StudentsForm(ModelForm):
    class Meta:
        model = Student
        fields = "__all__"

class CollegesForm(ModelForm):
    class Meta:
        model = College
        fields = "__all__"
