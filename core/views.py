
import os
from django.shortcuts import render
from django.conf import settings

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import logout
from .models import Course, Subject, Student, Marksheet
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.template.loader import render_to_string
from .forms import CenterForm


def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def courses(request):
    return render(request, 'courses/index.html')


def student_register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('student_register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        messages.success(request, "Registration successful. Please login.")
        return redirect('student_login')

    return render(request, 'student/register.html')


def student_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('admission_verification')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'student/login.html')


def student_logout(request):
    logout(request)
    return redirect('student_login')



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

from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404

from django.http import FileResponse, Http404

def download_receipt(request):
    enrollment_no = request.GET.get('enrollment_no')

    if not enrollment_no:
        raise Http404("Enrollment number required")

    student = get_object_or_404(Student, enrollment_no=enrollment_no)

    if not student.admission_receipt:
        raise Http404("Receipt not uploaded yet")

    return FileResponse(
        student.admission_receipt.open('rb'),
        as_attachment=True,
        filename=f"{student.enrollment_no}_Admission_Receipt.pdf"
    )



@login_required
def dashboard(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Access Denied")

    # Totals
    total_courses = Course.objects.count()
    total_subjects = Subject.objects.count()
    total_students = Student.objects.count()

    # Courses with number of subjects
    courses_with_subjects = Course.objects.annotate(subject_count=Count('subject'))
    course_subjects = [(c.name, c.subject_count) for c in courses_with_subjects]

    # ===== BAR CHART PERCENTAGES =====
    max_value = max(total_students, total_courses, total_subjects, 1)

    students_percent = (total_students / max_value) * 100
    courses_percent = (total_courses / max_value) * 100
    subjects_percent = (total_subjects / max_value) * 100

    context = {
        'total_courses': total_courses,
        'total_subjects': total_subjects,
        'total_students': total_students,
        'course_subjects': course_subjects,

        # chart values
        'students_percent': students_percent,
        'courses_percent': courses_percent,
        'subjects_percent': subjects_percent,
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
        course_name = request.POST.get('course_name', '').strip()
        course_code = request.POST.get('course_code', '').strip()
        course_duration = request.POST.get('course_duration', '').strip()
        course_fee = request.POST.get('course_fee', '').strip()

        if not course_name or not course_code:
            messages.error(request, "Course Name and Course Code are required!")
            return redirect('add_course')

        # Duplicate check (name OR code)
        if Course.objects.filter(name__iexact=course_name).exists():
            messages.warning(request, f"Course '{course_name}' already exists!")
        elif Course.objects.filter(code__iexact=course_code).exists():
            messages.warning(request, f"Course code '{course_code}' already exists!")
        else:
            Course.objects.create(
                name=course_name,
                code=course_code,
                duration=course_duration,
                fee=course_fee or 0
            )
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
        course_name = request.POST.get('course_name', '').strip()
        course_code = request.POST.get('course_code', '').strip()
        course_duration = request.POST.get('course_duration', '').strip()
        course_fee = request.POST.get('course_fee', '').strip()

        if not course_name or not course_code:
            messages.error(request, "Course Name and Course Code are required!")
            return redirect('edit_course', id=course.id)

        # Duplicate course code check (exclude current course)
        if Course.objects.filter(code__iexact=course_code).exclude(id=course.id).exists():
            messages.warning(request, f"Course code '{course_code}' already exists!")
            return redirect('edit_course', id=course.id)

        course.name = course_name
        course.code = course_code
        course.duration = course_duration
        course.fee = course_fee or 0
        course.save()

        messages.success(request, "Course updated successfully!")
        return redirect('add_course')

    return render(request, 'adminpanel/edit_course.html', {'course': course})


from .models import Center

def add_center(request):
    if request.method == "POST":
        form = CenterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Center details added successfully!")
            return redirect('add_center')
    else:
        form = CenterForm()

    centers = Center.objects.all()   # 👈 ye line missing thi

    return render(request, "adminpanel/add_center.html", {
        "form": form,
        "centers": centers
    })

def edit_center(request, id):
    center = get_object_or_404(Center, id=id)

    if request.method == "POST":
        form = CenterForm(request.POST, instance=center)
        if form.is_valid():
            form.save()
            messages.success(request, "Center updated successfully!")
            return redirect("add_center")
    else:
        form = CenterForm(instance=center)

    centers = Center.objects.all()
    return render(request, "adminpanel/add_center.html", {
        "form": form,
        "centers": centers
    })


def delete_center(request, id):
    center = get_object_or_404(Center, id=id)
    center.delete()
    messages.success(request, "Center deleted successfully!")
    return redirect("add_center")

def activate_center(request, id):
    Center.objects.update(is_active=False)   # sab inactive
    center = get_object_or_404(Center, id=id)
    center.is_active = True
    center.save()

    messages.success(request, "Center activated successfully!")
    return redirect('add_center')

@login_required
def add_subject(request):
    courses = Course.objects.all().order_by('name')
    subjects = Subject.objects.select_related('course').order_by('-id')

    if request.method == "POST":
        course_id = request.POST.get('course')
        theory_names = request.POST.getlist('theory_subjects[]')
        practical_names = request.POST.getlist('practical_subjects[]')

        # 🔒 Basic validation
        if not course_id:
            messages.error(request, "Please select a course.")
            return redirect('add_subject')

        if not any(theory_names) and not any(practical_names):
            messages.error(request, "Please enter at least one subject.")
            return redirect('add_subject')

        course = get_object_or_404(Course, id=course_id)

        # ==================================================
        # 🔹 ADD THEORY SUBJECTS
        # ==================================================
        added_count = 0
        for name in theory_names:
            name = name.strip()
            if not name:
                continue
            if Subject.objects.filter(course=course, name__iexact=name, type='theory').exists():
                messages.warning(
                    request,
                    f"'{name}' already exists in course '{course.name}' (Theory)."
                )
            else:
                Subject.objects.create(course=course, name=name, type='theory')
                added_count += 1

        # ==================================================
        # 🔹 ADD PRACTICAL SUBJECTS
        # ==================================================
        for name in practical_names:
            name = name.strip()
            if not name:
                continue
            if Subject.objects.filter(course=course, name__iexact=name, type='practical').exists():
                messages.warning(
                    request,
                    f"'{name}' already exists in course '{course.name}' (Practical)."
                )
            else:
                Subject.objects.create(course=course, name=name, type='practical')
                added_count += 1

        if added_count:
            messages.success(request, f"{added_count} subject(s) added successfully!")

        return redirect('add_subject')

    # ==================================================
    # 🔹 GET REQUEST
    # ==================================================
    return render(request, 'adminpanel/add_subject.html', {
        'courses': courses,
        'subjects': subjects,
    })


@login_required
def delete_subject(request, id):
    subject = get_object_or_404(Subject, id=id)
    subject.delete()
    messages.success(request, "Subject deleted successfully!")
    return redirect('add_subject')


@login_required
def edit_subject(request, id):
    subject = get_object_or_404(Subject, id=id)
    courses = Course.objects.all()

    if request.method == "POST":
        new_name = request.POST.get('subject_name').strip()
        course_id = request.POST.get('course')

        if not new_name:
            messages.error(request, "Subject name cannot be empty.")
            return redirect('edit_subject', id=id)

        # Duplicate check
        if Subject.objects.filter(course_id=course_id, name__iexact=new_name).exclude(id=subject.id).exists():
            messages.error(request, f"'{new_name}' already exists in this course.")
            return redirect('edit_subject', id=id)

        subject.name = new_name
        subject.course_id = course_id
        subject.save()
        messages.success(request, "Subject updated successfully!")
        return redirect('add_subject')

    return render(request, 'adminpanel/edit_subject.html', {
        'subject': subject,
        'courses': courses
    })

@login_required
def add_student(request):
    courses = Course.objects.all().order_by('name')

    if request.method == "POST":
        # Safe fetching
        name = (request.POST.get('name') or '').strip()
        email = (request.POST.get('email') or '').strip()
        phone = (request.POST.get('phone') or '').strip()
        father_name = (request.POST.get('father_name') or '').strip()
        address = (request.POST.get('address') or '').strip()
        session = (request.POST.get('course_session') or '').strip() 
        roll_no = (request.POST.get('roll_no') or '').strip()  # <-- fetch from POST

        course_id = request.POST.get('course')

        # Files
        tenth_marksheet = request.FILES.get('tenth_marksheet')
        twelfth_marksheet = request.FILES.get('twelfth_marksheet')
        aadhaar_card = request.FILES.get('aadhaar_card')
        photo = request.FILES.get('photo')

        # Validation
        if not course_id:
            messages.error(request, "Please select a course.")
            return redirect('add_student')
        if not name:
            messages.error(request, "Please enter student name.")
            return redirect('add_student')

        course = get_object_or_404(Course, id=course_id)

        # Create student
        student = Student(
            name=name,
            email=email,
            phone=phone,
            father_name=father_name,
            address=address,
            course=course,
            session=session,
            roll_no=roll_no, 

            tenth_marksheet=tenth_marksheet,
            twelfth_marksheet=twelfth_marksheet,
            aadhaar_card=aadhaar_card,
            photo=photo
        )
        student.save()  # course_code & duration auto-set
        messages.success(request, f"Student '{name}' added successfully!")
        return redirect('add_student')

    students = Student.objects.select_related('course').order_by('-id')
    return render(request, 'adminpanel/add_student.html', {
        'courses': courses,
        'students': students
    })


@login_required
def edit_student(request, id):
    student = get_object_or_404(Student, id=id)
    courses = Course.objects.all().order_by('name')

    if request.method == "POST":
        # ------------------------------
        # Safe fetching & strip
        # ------------------------------
        student.name = (request.POST.get('name') or '').strip()
        student.email = (request.POST.get('email') or '').strip()
        student.phone = (request.POST.get('phone') or '').strip()
        student.father_name = (request.POST.get('father_name') or '').strip()
        student.address = (request.POST.get('address') or '').strip()
        student.session = (request.POST.get('course_session') or '').strip()
        student.roll_no = (request.POST.get('roll_no') or '').strip()

        course_id = request.POST.get('course')
        if course_id:
            course = get_object_or_404(Course, id=course_id)
            student.course = course
            # course_code & duration auto-set in model's save()
        else:
            student.course = None
            student.course_code = ''
            student.duration = ''

        # ------------------------------
        # File updates (replace only if new file uploaded)
        # ------------------------------
        if request.FILES.get('tenth_marksheet'):
            student.tenth_marksheet = request.FILES.get('tenth_marksheet')
        if request.FILES.get('twelfth_marksheet'):
            student.twelfth_marksheet = request.FILES.get('twelfth_marksheet')
        if request.FILES.get('aadhaar_card'):
            student.aadhaar_card = request.FILES.get('aadhaar_card')
        if request.FILES.get('photo'):
            student.photo = request.FILES.get('photo')

        # ------------------------------
        # Save
        # ------------------------------
        student.save()
        messages.success(request, f"Student '{student.name}' updated successfully!")
        return redirect('add_student')

    return render(request, 'adminpanel/edit_student.html', {
        'student': student,
        'courses': courses
    })

# Delete Student View
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    student.delete()
    messages.success(request, f"{student.name} deleted successfully!")
    return redirect('add_student')


from django.core.files.base import ContentFile
from io import BytesIO

@login_required
def download_admission_receipt(request, student_id):
    import os
    from io import BytesIO
    from django.core.files.base import ContentFile
    from django.conf import settings
    from xhtml2pdf import pisa

    student = get_object_or_404(Student, id=student_id)
    center = Center.objects.filter(is_active=True).first()  # Ensure at least one active center

    # Absolute paths for logos
    left_logo_path = os.path.join(settings.BASE_DIR, 'static/images/logo.png')
    right_logo_path = os.path.join(settings.BASE_DIR, 'static/images/right_logo.png')
    left_logo_url = left_logo_path.replace('\\','/')
    right_logo_url = right_logo_path.replace('\\','/')

    # Course fees
    course_fee = student.course.fee if student.course else 0
    fees = {
        'course': course_fee,
        'registration': 0,
        'exam': 0,
        'paid': course_fee,
    }

    html = render_to_string(
        'adminpanel/admission_receipt.html',
        {
            'student': student,
            'fees': fees,
            'center': center,
            'left_logo_url': left_logo_url,
            'right_logo_url': right_logo_url,
        }
    )

    result = BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=result)

    if pisa_status.err:
        return HttpResponse("PDF generation failed")

    filename = f"Admission_Receipt_{student.enrollment_no}.pdf"
    student.admission_receipt.save(
        filename,
        ContentFile(result.getvalue()),
        save=True
    )

    response = HttpResponse(result.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response

@login_required
def add_marksheet(request):
    students = Student.objects.select_related('course').all().order_by('roll_no')
    saved_marksheets = Marksheet.objects.select_related('student').order_by('-id')

    marksheets_with_totals = []
    for m in saved_marksheets:
        marks = m.marks
        theory_total = {'full': 0, 'pass': 0, 'obtained': 0}
        practical_total = {'full': 0, 'pass': 0, 'obtained': 0}

        # Calculate totals
        for data in marks.get('theory', {}).values():
            theory_total['full'] += data.get('full', 0)
            theory_total['pass'] += data.get('pass', 0)
            theory_total['obtained'] += data.get('obtained', 0)

        for data in marks.get('practical', {}).values():
            practical_total['full'] += data.get('full', 0)
            practical_total['pass'] += data.get('pass', 0)
            practical_total['obtained'] += data.get('obtained', 0)

        # Grand total
        grand_full = theory_total['full'] + practical_total['full']
        grand_pass = theory_total['pass'] + practical_total['pass']
        grand_obtained = theory_total['obtained'] + practical_total['obtained']

        # Percentage
        percentage = (grand_obtained / grand_full * 100) if grand_full > 0 else 0

        # Division
        if percentage >= 60:
            division = "First"
        elif percentage >= 45:
            division = "Second"
        elif percentage >= 33:
            division = "Third"
        else:
            division = "Fail"

        marksheets_with_totals.append({
            'marksheet': m,
            'theory_total': theory_total,
            'practical_total': practical_total,
            'grand_total': grand_obtained,
            'grand_full': grand_full,
            'percentage': round(percentage, 2),
            'division': division
        })

    if request.method == "POST":
        roll_no = request.POST.get('roll_no')
        if not roll_no:
            messages.error(request, "Please select a student.")
            return redirect('add_marksheet')

        student = get_object_or_404(Student, id=roll_no)
        marks_dict = {"theory": {}, "practical": {}}

        for key in request.POST:
            if key.startswith('obtained[') and key.endswith(']'):
                sub_name = key[9:-1]
                sub_type = request.POST.get(f"type[{sub_name}]")
                full_mark = request.POST.get(f"full[{sub_name}]")
                pass_mark = request.POST.get(f"pass[{sub_name}]")
                obtained_mark = request.POST.get(f"obtained[{sub_name}]")

                if sub_type == 'theory':
                    marks_dict['theory'][sub_name] = {
                        'full': int(full_mark),
                        'pass': int(pass_mark),
                        'obtained': int(obtained_mark)
                    }
                else:
                    marks_dict['practical'][sub_name] = {
                        'full': int(full_mark),
                        'pass': int(pass_mark),
                        'obtained': int(obtained_mark)
                    }

        uploaded_file = request.FILES.get('file')

        Marksheet.objects.create(
            student=student,
            marks=marks_dict,
            file=uploaded_file
        )

        messages.success(request, f"Marksheet for {student.name} saved successfully!")
        return redirect('add_marksheet')

    return render(request, 'adminpanel/add_marksheet.html', {
        'students': students,
        'marksheets_with_totals': marksheets_with_totals
    })


@login_required
def edit_marksheet(request, pk):
    m = get_object_or_404(Marksheet, pk=pk)
    students = Student.objects.select_related('course').all().order_by('roll_no')

    if request.method == "POST":
        # Update marks
        theory = {}
        practical = {}
        for key in request.POST:
            if key.startswith('marks[') and key.endswith(']'):
                sub_name = key[6:-1]
                sub_type = request.POST.get(f"type[{sub_name}]")
                if sub_type == 'theory':
                    theory[sub_name] = int(request.POST[key])
                else:
                    practical[sub_name] = int(request.POST[key])

        m.marks = {"theory": theory, "practical": practical}

        # Update file if new file uploaded
        uploaded_file = request.FILES.get('file')
        if uploaded_file:
            m.file = uploaded_file

        m.save()
        messages.success(request, "Marksheet updated successfully!")
        return redirect('add_marksheet')

    return render(request, 'adminpanel/edit_marksheet.html', {
        'marksheet': m,
        'students': students
    })


@login_required
def delete_marksheet(request, pk):
    m = get_object_or_404(Marksheet, pk=pk)
    if request.method == "POST":
        m.delete()
        messages.success(request, "Marksheet deleted successfully!")
        return redirect('add_marksheet')
    return render(request, 'adminpanel/delete_marksheet_confirm.html', {"marksheet": m})



@login_required
def download_marksheet(request, enrollment_no):

    student = get_object_or_404(Student, enrollment_no=enrollment_no)

    marksheet = (
        Marksheet.objects
        .filter(student=student)
        .order_by('-uploaded_at')
        .first()
    )

    if not marksheet:
        return HttpResponse("No marksheet found")

    center = Center.objects.filter(is_active=True).first()

    # Logos
    left_logo_path = os.path.join(settings.BASE_DIR, 'static/images/logo.png')
    right_logo_path = os.path.join(settings.BASE_DIR, 'static/images/right_logo.png')

    left_logo_url = left_logo_path.replace('\\', '/')
    right_logo_url = right_logo_path.replace('\\', '/')

    # Totals calculation
    theory_full = theory_pass = theory_obt = 0
    practical_full = practical_pass = practical_obt = 0

    # Theory totals
    if marksheet.marks.get('theory'):
        for v in marksheet.marks['theory'].values():
            theory_full += int(v.get('full', 0))
            theory_pass += int(v.get('pass', 0))
            theory_obt += int(v.get('obtained', 0))

    # Practical totals
    if marksheet.marks.get('practical'):
        for v in marksheet.marks['practical'].values():
            practical_full += int(v.get('full', 0))
            practical_pass += int(v.get('pass', 0))
            practical_obt += int(v.get('obtained', 0))

    # Grand totals
    grand_full = theory_full + practical_full
    grand_pass = theory_pass + practical_pass
    grand_total = theory_obt + practical_obt
    percentage = round((grand_total / grand_full) * 100, 2) if grand_full else 0

    # Division
    if percentage >= 60:
        division = "First"
    elif percentage >= 45:
        division = "Second"
    elif percentage >= 33:
        division = "Third"
    else:
        division = "Fail"

    context = {
        'student': student,
        'marksheet': marksheet,
        'center': center,
        'theory_full': theory_full,
        'theory_pass': theory_pass,           # ✅ Pass total added
        'theory_obt': theory_obt,
        'practical_full': practical_full,
        'practical_pass': practical_pass,     # ✅ Pass total added
        'practical_obt': practical_obt,
        'grand_full': grand_full,
        'grand_pass': grand_pass,             # ✅ Grand pass total
        'grand_total': grand_total,
        'percentage': percentage,
        'division': division,
        'left_logo_url': left_logo_url,
        'right_logo_url': right_logo_url,
    }

    html = render_to_string('adminpanel/marksheet.html', context)

    result = BytesIO()
    pdf = pisa.CreatePDF(html, dest=result)

    if pdf.err:
        return HttpResponse("PDF generation error")

    response = HttpResponse(result.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = (
        f'attachment; filename="Marksheet_{student.enrollment_no}.pdf"'
    )
    return response


from django.http import JsonResponse

def api_verify_admission(request):
    if request.method == "POST":
        enrollment_no = request.POST.get("enrollment_no", "").strip()
        if not enrollment_no:
            return JsonResponse({"error": "Enrollment ID required"}, status=400)

        try:
            student = Student.objects.get(enrollment_no=enrollment_no)
        except Student.DoesNotExist:
            return JsonResponse([], safe=False)  # No record found

        data = {
            "studentName": student.name,
            "fathersName": student.father_name,
            "enrollment_no": student.enrollment_no,
            "rollNumber": student.roll_no,
            "courseName": student.course.name if student.course else "",
            "courseCode": student.course_code,
            "courseDuration": student.duration,
            "session": student.session,
            "centerName": student.center_name or "",
            "centerCode": student.center_code or "",
            "centerAddress": student.center_address or "",
            "admissionDate": student.created_at.strftime("%Y-%m-%d"),
            "photoPath": student.photo.name if student.photo else "",
            "receiptUrl": student.admission_receipt.url if student.admission_receipt else None
        }
        return JsonResponse([data], safe=False)

def admin_logout(request):
    logout(request)
    return redirect('home')  