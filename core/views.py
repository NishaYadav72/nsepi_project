from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import logout
from .models import Course, Subject, Student
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count


def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def courses(request):
    return render(request, 'courses/index.html')


def student_login(request):
    return render(request, 'studentzone/student-login.html')

def admission_verification(request):
    return render(request, 'studentzone/verify-addmission.html')

def admit_card(request):
    return render(request, 'admit_card.html')

def verify_certificate(request):
    return render(request, 'verify_certificate.html')

def student_result(request):
    return render(request, 'student/result.html')


def placements(request):
    return render(request, 'placements.html')

def branches(request):
    return render(request, 'branches.html')

def contact(request):
    return render(request, 'contact.html')

def branch_application(request):
    return render(request, 'branch-application.html')



def electrical(request):
    return render(request, 'courses/electrical.html') 

def ac_and_refrigeration(request):
    return render(request, 'courses/ac-and-refrigeration.html') 

def automobile(request):
    return render(request, 'courses/automobile.html')

def mechanical_turner_fitter_cnc(request):
    return render(request, 'courses/mechanical-turner-fitter-cnc.html')

def computer_hardware_and_networking(request):
    return render(request, 'courses/computer-hardware-and-networking.html')

def smart_phone_technician(request):
    return render(request, 'courses/smart-phone-technician.html')

def computer_softwares(request):
    return render(request, 'courses/computer-softwares.html')

def computer_softwares(request):
    return render(request, 'courses/computer-softwares.html')

def fashion_design_and_tailoring(request):
    return render(request, 'courses/fashion-design-and-tailoring.html')


def beautician(request):
    return render(request, 'courses/beautician.html')

def soft_skills(request):
    return render(request, 'courses/soft-skills.html')

def teacher_training(request):
    return render(request, 'courses/teacher-training.html')

def paramedical(request):
    return render(request, 'courses/paramedical.html')

def amanat_training(request):
    return render(request, 'courses/amanat-training.html')

def fire_and_safety_management(request):
    return render(request, 'courses/fire-and-safety-management.html')

def terms_and_conditions(request):
    return render(request, 'terms-and-conditions.html')

def privacy_policy(request):
    return render(request, 'privacy-policy.html')

def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect("dashboard")
            else:
                return render(request, "admin_login.html", {
                    "error": "You are not authorized as Admin"
                })
        else:
            return render(request, "admin_login.html", {
                "error": "Invalid username or password"
            })

    return render(request, "admin_login.html")

@login_required
def dashboard(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Access Denied")

    return render(request, "dashboard.html")


@login_required
def dashboard(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Access Denied")

    total_courses = Course.objects.count()
    total_subjects = Subject.objects.count()
    total_students = Student.objects.count()

    # Courses with number of subjects
    courses_with_subjects = Course.objects.annotate(subject_count=Count('subject'))
    course_subjects = [(c.name, c.subject_count) for c in courses_with_subjects]

    context = {
        'total_courses': total_courses,
        'total_subjects': total_subjects,
        'total_students': total_students,
        'course_subjects': course_subjects
    }

    return render(request, 'adminpanel/dashboard.html', context)


@login_required
def admin_profile(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        if password:
            request.user.set_password(password)
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Password updated successfully')
            return redirect('admin_profile')

    return render(request, 'adminpanel/profile.html')



@login_required
def add_course(request):
    if request.method == "POST":
        course_name = request.POST.get('course_name').strip()
        if course_name:
            # Check if course already exists (case-insensitive)
            if Course.objects.filter(name__iexact=course_name).exists():
                messages.warning(request, f"Course '{course_name}' already exists!")
            else:
                Course.objects.create(name=course_name)
                messages.success(request, f"Course '{course_name}' added successfully!")
        return redirect('add_course')

    courses = Course.objects.all().order_by('-id')
    return render(request, 'adminpanel/add_course.html', {'courses': courses})

@login_required
def delete_course(request, id):
    course = get_object_or_404(Course, id=id)
    course.delete()
    return redirect('add_course')

@login_required
def edit_course(request, id):
    course = get_object_or_404(Course, id=id)

    if request.method == "POST":
        course.name = request.POST.get('course_name')
        course.save()
        return redirect('add_course')

    return render(request, 'adminpanel/edit_course.html', {'course': course})

@login_required
def add_subject(request):
    courses = Course.objects.all()
    subjects = Subject.objects.select_related('course')

    if request.method == "POST":
        course_id = request.POST.get('course')
        subject_names = request.POST.getlist('subjects[]')  # multiple subjects

        if course_id and subject_names:
            course = Course.objects.get(id=course_id)
            added_any = False

            for name in subject_names:
                name = name.strip()
                if not Subject.objects.filter(course=course, name__iexact=name).exists():
                    Subject.objects.create(course=course, name=name)
                    added_any = True
                else:
                    messages.warning(request, f"'{name}' is already added for course '{course.name}'")

            if added_any:
                messages.success(request, "Subjects added successfully!")

            return redirect('add_subject')

    return render(request, 'adminpanel/add_subject.html', {
        'courses': courses,
        'subjects': subjects
    })

@login_required
def delete_subject(request, id):
    subject = get_object_or_404(Subject, id=id)
    subject.delete()
    return redirect('add_subject')

@login_required
def edit_subject(request, id):
    subject = get_object_or_404(Subject, id=id)
    courses = Course.objects.all()

    if request.method == "POST":
        subject.name = request.POST.get('subject_name')
        subject.course_id = request.POST.get('course')
        subject.save()
        return redirect('add_subject')

    return render(request, 'adminpanel/edit_subject.html', {
        'subject': subject,
        'courses': courses
    })

@login_required
def add_student(request):
    courses = Course.objects.all()  # <-- fetch all courses

    if request.method == "POST":
        Student.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            father_name=request.POST.get('father_name'),
            address=request.POST.get('address'),
            tenth_marksheet=request.FILES.get('tenth_marksheet'),
            twelfth_marksheet=request.FILES.get('twelfth_marksheet'),
            aadhaar_card=request.FILES.get('aadhaar_card'),  
            photo=request.FILES.get('photo'),
        )
        return redirect('add_student')

    students = Student.objects.all().order_by('-id')
    return render(request, 'adminpanel/add_student.html', {
        'students': students,
        'courses': courses

    })

def edit_student(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        student.name = request.POST.get('name')
        student.email = request.POST.get('email')
        student.phone = request.POST.get('phone')
        student.father_name = request.POST.get('father_name')
        student.address = request.POST.get('address')

        if request.FILES.get('tenth_marksheet'):
            student.tenth_marksheet = request.FILES.get('tenth_marksheet')
        if request.FILES.get('twelfth_marksheet'):
            student.twelfth_marksheet = request.FILES.get('twelfth_marksheet')
        if request.FILES.get('aadhaar_card'):
            student.aadhaar_card = request.FILES.get('aadhaar_card')
        if request.FILES.get('photo'):
            student.photo = request.FILES.get('photo')

        student.save()
        messages.success(request, f"{student.name} updated successfully!")
        return redirect('add_student')

    return render(request, 'adminpanel/edit_student.html', {'student': student})


# Delete Student View
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    student.delete()
    messages.success(request, f"{student.name} deleted successfully!")
    return redirect('add_student')

def admin_logout(request):
    logout(request)
    return redirect('home')  