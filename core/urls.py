from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('courses/', views.courses, name='courses'),

    path('student/login/', views.student_login, name='student_login'),
    path('student/admission-verification/', views.admission_verification, name='admission_verification'),
    path('student/admit-card/', views.admit_card, name='admit_card'),
    path('student/verify-certificate/', views.verify_certificate, name='verify_certificate'),
    path('student/result/', views.student_result, name='student_result'),
    path('placements/', views.placements, name='placements'),
    path('branches/', views.branches, name='branches'),
    path('contact/', views.contact, name='contact'),
    path('branch-application/', views.branch_application, name='branch_application'),



    path('courses/electrical/', views.electrical, name='electrical'),
    path('courses/ac-and-refrigeration/', views.ac_and_refrigeration, name='ac_and_refrigeration'),
    path('courses/automobile/', views.automobile, name='automobile'),
    path('courses/mechanical-turner-fitter-cnc/', views.mechanical_turner_fitter_cnc, name='mechanical_turner_fitter_cnc'),
    path('courses/computer-hardware-and-networking/', views.computer_hardware_and_networking, name='computer_hardware_and_networking'),
    path('courses/smart-phone-technician/', views.smart_phone_technician, name='smart_phone_technician'),
path('courses/computer-softwares/',views.computer_softwares,name='computer_softwares'),
path(
    'courses/computer-softwares/',
    views.computer_softwares,
    name='computer_softwares'
),

path(
    'courses/fashion-design-and-tailoring/',
    views.fashion_design_and_tailoring,
    name='fashion_design_and_tailoring'
),

path(
    'courses/beautician/',
    views.beautician,
    name='beautician'
),

path(
    'courses/soft-skills/',
    views.soft_skills,
    name='soft_skills'
),

path(
    'courses/teacher-training/',
    views.teacher_training,
    name='teacher_training'
),

path(
    'courses/paramedical/',
    views.paramedical,
    name='paramedical'
),

path(
    'courses/amanat-training/',
    views.amanat_training,
    name='amanat_training'
),

path(
    'courses/fire-and-safety-management/',
    views.fire_and_safety_management,
    name='fire_and_safety_management'
),


path("admin-login/", views.admin_login, name="admin_login"),
path('dashboard/', views.dashboard, name='dashboard'),
path('profile/', views.admin_profile, name='admin_profile'),
path('add-course/', views.add_course, name='add_course'),
path('delete-course/<int:id>/', views.delete_course, name='delete_course'),
path('edit-course/<int:id>/', views.edit_course, name='edit_course'),

path('add-subject/', views.add_subject, name='add_subject'),
path('delete-subject/<int:id>/', views.delete_subject, name='delete_subject'),
path('edit-subject/<int:id>/', views.edit_subject, name='edit_subject'),

path('add-student/', views.add_student, name='add_student'),
path('edit-student/<int:id>/', views.edit_student, name='edit_student'),
path('delete-student/<int:id>/', views.delete_student, name='delete_student'),

path('logout/', views.admin_logout, name='logout'),

]
