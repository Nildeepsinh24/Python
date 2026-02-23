from django.contrib import admin

from .models import Student, Course


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
	list_display = ("first_name", "last_name", "email")
	search_fields = ("first_name", "last_name", "email")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
	list_display = ("code", "title")
	search_fields = ("code", "title")
