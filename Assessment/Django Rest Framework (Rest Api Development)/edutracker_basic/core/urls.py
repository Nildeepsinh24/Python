from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("students/", views.students_page, name="students_page"),
    path("students/<int:student_id>/", views.student_detail_page, name="student_detail_page"),
    path("students/<int:student_id>/update/", views.student_update, name="student_update"),
    path("students/<int:student_id>/delete/", views.student_delete, name="student_delete"),
    path("students/<int:student_id>/enroll/", views.student_enroll, name="student_enroll"),
    path(
        "students/<int:student_id>/unenroll/<int:course_id>/",
        views.student_unenroll,
        name="student_unenroll",
    ),
    path("courses/", views.courses_page, name="courses_page"),
    path("courses/<int:course_id>/", views.course_detail_page, name="course_detail_page"),
    path("courses/<int:course_id>/update/", views.course_update, name="course_update"),
    path("courses/<int:course_id>/delete/", views.course_delete, name="course_delete"),
]
