from django.urls import path

from . import views

urlpatterns = [
	path("students/", views.students, name="api_students"),
	path("students/<int:student_id>/", views.student_detail, name="api_student_detail"),
	path("students/<int:student_id>/enroll/", views.enroll_course, name="api_enroll_course"),
	path("students/<int:student_id>/unenroll/", views.unenroll_course, name="api_unenroll_course"),
	path("courses/", views.courses, name="api_courses"),
	path("courses/<int:course_id>/", views.course_detail, name="api_course_detail"),
]
