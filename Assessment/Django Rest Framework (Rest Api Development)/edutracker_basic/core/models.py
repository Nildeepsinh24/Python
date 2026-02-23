from django.db import models


class Course(models.Model):
	title = models.CharField(max_length=200)
	code = models.CharField(max_length=50, unique=True)
	description = models.TextField(blank=True)

	def __str__(self):
		return f"{self.code} - {self.title}"


class Student(models.Model):
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	email = models.EmailField(unique=True)
	created_at = models.DateTimeField(auto_now_add=True)
	courses = models.ManyToManyField(Course, related_name="students", blank=True)

	def __str__(self):
		return f"{self.first_name} {self.last_name}"
