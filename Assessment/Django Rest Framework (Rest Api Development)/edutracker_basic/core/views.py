import json

from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .forms import StudentForm, CourseForm
from .models import Student, Course


def _parse_json(request):
	if not request.body:
		return {}
	try:
		return json.loads(request.body.decode("utf-8"))
	except json.JSONDecodeError:
		return None


def _course_to_dict(course):
	return {
		"id": course.id,
		"title": course.title,
		"code": course.code,
		"description": course.description,
	}


def _student_to_dict(student):
	return {
		"id": student.id,
		"first_name": student.first_name,
		"last_name": student.last_name,
		"email": student.email,
		"created_at": student.created_at.isoformat(),
		"courses": [_course_to_dict(course) for course in student.courses.all()],
	}


def home(request):
	student_count = Student.objects.count()
	course_count = Course.objects.count()
	return render(
		request,
		"core/home.html",
		{
			"student_count": student_count,
			"course_count": course_count,
		},
	)


def students_page(request):
	if request.method == "POST":
		form = StudentForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect("students_page")
	else:
		form = StudentForm()

	students_list = Student.objects.all()
	return render(
		request,
		"core/students.html",
		{
			"form": form,
			"students": students_list,
		},
	)


def student_detail_page(request, student_id):
	student = get_object_or_404(Student, id=student_id)
	form = StudentForm(instance=student)
	enrolled = student.courses.all()
	available = Course.objects.exclude(id__in=enrolled.values_list("id", flat=True))
	return render(
		request,
		"core/student_detail.html",
		{
			"student": student,
			"form": form,
			"enrolled": enrolled,
			"available": available,
		},
	)


@require_POST
def student_update(request, student_id):
	student = get_object_or_404(Student, id=student_id)
	form = StudentForm(request.POST, instance=student)
	if form.is_valid():
		form.save()
		return redirect("student_detail_page", student_id=student.id)

	return render(
		request,
		"core/student_detail.html",
		{
			"student": student,
			"form": form,
			"enrolled": student.courses.all(),
			"available": Course.objects.exclude(
				id__in=student.courses.values_list("id", flat=True)
			),
		},
	)


@require_POST
def student_delete(request, student_id):
	student = get_object_or_404(Student, id=student_id)
	student.delete()
	return redirect("students_page")


@require_POST
def student_enroll(request, student_id):
	student = get_object_or_404(Student, id=student_id)
	course_id = request.POST.get("course_id")
	if course_id:
		course = get_object_or_404(Course, id=course_id)
		student.courses.add(course)
	return redirect("student_detail_page", student_id=student.id)


@require_POST
def student_unenroll(request, student_id, course_id):
	student = get_object_or_404(Student, id=student_id)
	course = get_object_or_404(Course, id=course_id)
	student.courses.remove(course)
	return redirect("student_detail_page", student_id=student.id)


def courses_page(request):
	if request.method == "POST":
		form = CourseForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect("courses_page")
	else:
		form = CourseForm()

	courses_list = Course.objects.all()
	return render(
		request,
		"core/courses.html",
		{
			"form": form,
			"courses": courses_list,
		},
	)


def course_detail_page(request, course_id):
	course = get_object_or_404(Course, id=course_id)
	form = CourseForm(instance=course)
	students_list = course.students.all()
	return render(
		request,
		"core/course_detail.html",
		{
			"course": course,
			"form": form,
			"students": students_list,
		},
	)


@require_POST
def course_update(request, course_id):
	course = get_object_or_404(Course, id=course_id)
	form = CourseForm(request.POST, instance=course)
	if form.is_valid():
		form.save()
		return redirect("course_detail_page", course_id=course.id)

	return render(
		request,
		"core/course_detail.html",
		{
			"course": course,
			"form": form,
			"students": course.students.all(),
		},
	)


@require_POST
def course_delete(request, course_id):
	course = get_object_or_404(Course, id=course_id)
	course.delete()
	return redirect("courses_page")


@csrf_exempt
def students(request):
	# Content negotiation: serve HTML landing page if Accept header includes text/html
	accept_header = request.headers.get("Accept", "")
	if "text/html" in accept_header and request.method == "GET":
		# Check if it's a browser request (not a JSON request)
		if "application/json" not in accept_header or accept_header.index("text/html") < accept_header.index("application/json"):
			return render(request, "core/api_students.html")
	
	if request.method == "GET":
		data = [_student_to_dict(student) for student in Student.objects.all()]
		return JsonResponse({"results": data})

	if request.method == "POST":
		payload = _parse_json(request)
		if payload is None:
			return JsonResponse({"error": "Invalid JSON"}, status=400)

		required = ["first_name", "last_name", "email"]
		missing = [field for field in required if field not in payload]
		if missing:
			return JsonResponse({"error": f"Missing fields: {', '.join(missing)}"}, status=400)

		student = Student.objects.create(
			first_name=payload["first_name"],
			last_name=payload["last_name"],
			email=payload["email"],
		)
		return JsonResponse(_student_to_dict(student), status=201)

	return HttpResponseNotAllowed(["GET", "POST"])


@csrf_exempt
def student_detail(request, student_id):
	try:
		student = Student.objects.get(id=student_id)
	except Student.DoesNotExist:
		return JsonResponse({"error": "Student not found"}, status=404)

	if request.method == "GET":
		return JsonResponse(_student_to_dict(student))

	if request.method == "PUT":
		payload = _parse_json(request)
		if payload is None:
			return JsonResponse({"error": "Invalid JSON"}, status=400)

		for field in ["first_name", "last_name", "email"]:
			if field in payload:
				setattr(student, field, payload[field])
		student.save()
		return JsonResponse(_student_to_dict(student))

	if request.method == "DELETE":
		student.delete()
		return JsonResponse({"message": "Student deleted"})

	return HttpResponseNotAllowed(["GET", "PUT", "DELETE"])


@csrf_exempt
def courses(request):
	# Content negotiation: serve HTML landing page if Accept header includes text/html
	accept_header = request.headers.get("Accept", "")
	if "text/html" in accept_header and request.method == "GET":
		# Check if it's a browser request (not a JSON request)
		if "application/json" not in accept_header or accept_header.index("text/html") < accept_header.index("application/json"):
			return render(request, "core/api_courses.html")
	
	if request.method == "GET":
		data = [_course_to_dict(course) for course in Course.objects.all()]
		return JsonResponse({"results": data})

	if request.method == "POST":
		payload = _parse_json(request)
		if payload is None:
			return JsonResponse({"error": "Invalid JSON"}, status=400)

		required = ["title", "code"]
		missing = [field for field in required if field not in payload]
		if missing:
			return JsonResponse({"error": f"Missing fields: {', '.join(missing)}"}, status=400)

		course = Course.objects.create(
			title=payload["title"],
			code=payload["code"],
			description=payload.get("description", ""),
		)
		return JsonResponse(_course_to_dict(course), status=201)

	return HttpResponseNotAllowed(["GET", "POST"])


@csrf_exempt
def course_detail(request, course_id):
	try:
		course = Course.objects.get(id=course_id)
	except Course.DoesNotExist:
		return JsonResponse({"error": "Course not found"}, status=404)

	if request.method == "GET":
		return JsonResponse(_course_to_dict(course))

	if request.method == "PUT":
		payload = _parse_json(request)
		if payload is None:
			return JsonResponse({"error": "Invalid JSON"}, status=400)

		for field in ["title", "code", "description"]:
			if field in payload:
				setattr(course, field, payload[field])
		course.save()
		return JsonResponse(_course_to_dict(course))

	if request.method == "DELETE":
		course.delete()
		return JsonResponse({"message": "Course deleted"})

	return HttpResponseNotAllowed(["GET", "PUT", "DELETE"])


@csrf_exempt
def enroll_course(request, student_id):
	if request.method != "POST":
		return HttpResponseNotAllowed(["POST"])

	payload = _parse_json(request)
	if payload is None:
		return JsonResponse({"error": "Invalid JSON"}, status=400)

	course_id = payload.get("course_id")
	if not course_id:
		return JsonResponse({"error": "course_id is required"}, status=400)

	try:
		student = Student.objects.get(id=student_id)
	except Student.DoesNotExist:
		return JsonResponse({"error": "Student not found"}, status=404)

	try:
		course = Course.objects.get(id=course_id)
	except Course.DoesNotExist:
		return JsonResponse({"error": "Course not found"}, status=404)

	student.courses.add(course)
	return JsonResponse({"message": "Course linked", "student": _student_to_dict(student)})


@csrf_exempt
def unenroll_course(request, student_id):
	if request.method != "POST":
		return HttpResponseNotAllowed(["POST"])

	payload = _parse_json(request)
	if payload is None:
		return JsonResponse({"error": "Invalid JSON"}, status=400)

	course_id = payload.get("course_id")
	if not course_id:
		return JsonResponse({"error": "course_id is required"}, status=400)

	try:
		student = Student.objects.get(id=student_id)
	except Student.DoesNotExist:
		return JsonResponse({"error": "Student not found"}, status=404)

	try:
		course = Course.objects.get(id=course_id)
	except Course.DoesNotExist:
		return JsonResponse({"error": "Course not found"}, status=404)

	student.courses.remove(course)
	return JsonResponse({"message": "Course unlinked", "student": _student_to_dict(student)})
