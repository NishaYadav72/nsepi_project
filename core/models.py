import random
from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
# Create your models here.


class Subject(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name} ({self.course.name})"
    
def generate_registration_id():
    return f"NSEPI/BR212/{random.randint(100000, 999999)}"

class Student(models.Model):
    registration_id = models.CharField(
        max_length=30,
        unique=True,
        editable=False,
        default=generate_registration_id
    )

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    father_name = models.CharField(max_length=100)
    address = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)

    tenth_marksheet = models.ImageField(
        upload_to='students/10th/',
        null=True,
        blank=True
    )

    twelfth_marksheet = models.ImageField(
        upload_to='students/12th/',
        null=True,
        blank=True
    )

    aadhaar_card = models.ImageField(
        upload_to='students/aadhaar/',
        null=True,
        blank=True
    )

    photo = models.ImageField(
        upload_to='students/photo/',
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.registration_id})"
