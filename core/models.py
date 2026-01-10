import random
from django.db import models
from django.contrib.postgres.fields import JSONField

class Course(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True, null=True, blank=True)
    duration = models.CharField(max_length=100, null=True, blank=True)
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name


class Subject(models.Model):

    YEAR_CHOICES = (
        ('first', 'First Year'),
        ('second', 'Second Year'),
    )

    TYPE_CHOICES = (
        ('theory', 'Theory'),
        ('practical', 'Practical'),
    )

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    year = models.CharField(max_length=10, choices=YEAR_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.course.name}) - {self.get_year_display()}"

class Center(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50)
    address = models.TextField()

    is_active = models.BooleanField(default=True)  # ⭐ IMPORTANT

    def __str__(self):
        return f"{self.name} ({self.code})"

def generate_enrollment_no():
    return f"NSEPI/BR212/{random.randint(100000, 999999)}"

# ===============================
# Student Model
# ===============================
class Student(models.Model):
    enrollment_no = models.CharField(
        max_length=30,
        unique=True,
        editable=False,
        default=generate_enrollment_no
    )

    # Basic Info
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    father_name = models.CharField(max_length=100)
    address = models.TextField()

    # Course
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    course_code = models.CharField(max_length=50, blank=True, null=True)
    duration = models.CharField(max_length=50, blank=True, null=True)
    session = models.CharField(max_length=50, blank=True, null=True)
    roll_no = models.CharField(max_length=50, blank=True, null=True)


    # Documents
    tenth_marksheet = models.ImageField(
        upload_to='students/10th/', null=True, blank=True
    )
    twelfth_marksheet = models.ImageField(
        upload_to='students/12th/', null=True, blank=True
    )
    aadhaar_card = models.ImageField(
        upload_to='students/aadhaar/', null=True, blank=True
    )
    photo = models.ImageField(
        upload_to='students/photo/', null=True, blank=True
    )

# New fields for center info
    center_name = models.CharField(max_length=255, blank=True, null=True)
    center_code = models.CharField(max_length=50, blank=True, null=True)
    center_address = models.TextField(blank=True, null=True)

    # ✅ Admission Receipt PDF
    admission_receipt = models.FileField(
        upload_to='admission_receipts/',
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    # ===============================
    # Auto-fill course code & duration
    # ===============================
    def save(self, *args, **kwargs):
        if self.course:
            self.course_code = self.course.code
            self.duration = self.course.duration
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.enrollment_no})"


class Marksheet(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    marks = models.JSONField()
    file = models.FileField(upload_to='marksheets/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    YEAR_CHOICES = (
        ('first', 'First Year'),
        ('second', 'Second Year'),
    )
    year = models.CharField(max_length=10, choices=YEAR_CHOICES, default='first')  # ✅ add this

    def __str__(self):
        return f"{self.student.name} - {self.get_year_display()} Marks"
