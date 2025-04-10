from django.forms import ModelForm
from django import forms
from .models import Organization, OrgMember, Student, College, Program

class OrganizationForm(ModelForm):
    class Meta:
        model = Organization
        fields = "__all__"

class OrgMembersForm(ModelForm):
    class Meta:
        model = OrgMember
        fields = "__all__"
        widgets = {
            'date_joined': forms.DateInput(attrs={'type': 'date'}),
        }

class StudentsForm(ModelForm):
    class Meta:
        model = Student
        fields = "__all__"

class CollegesForm(ModelForm):
    class Meta:
        model = College
        fields = "__all__"


class ProgramsForm(ModelForm):
    class Meta:
        model = Program
        fields = "__all__"
