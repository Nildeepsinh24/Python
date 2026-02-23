from django import forms

from .models import Student, Course


class StudentForm(forms.ModelForm):
	class Meta:
		model = Student
		fields = ["first_name", "last_name", "email"]
		widgets = {
			"first_name": forms.TextInput(attrs={"class": "form-control"}),
			"last_name": forms.TextInput(attrs={"class": "form-control"}),
			"email": forms.EmailInput(attrs={"class": "form-control"}),
		}


class CourseForm(forms.ModelForm):
	class Meta:
		model = Course
		fields = ["title", "code", "description"]
		widgets = {
			"title": forms.TextInput(attrs={"class": "form-control"}),
			"code": forms.TextInput(attrs={"class": "form-control"}),
			"description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
		}
