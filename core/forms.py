from django.contrib import admin
from django.utils.html import format_html
from .models import Marksheet
from .models import Center
from django import forms


@admin.register(Marksheet)
class MarksheetAdmin(admin.ModelAdmin):
    list_display = ('student', 'show_marks', 'uploaded_at')
    list_filter = ('uploaded_at', 'student')
    search_fields = ('student__name', 'student__roll_no')

    def show_marks(self, obj):
        html = ""
        for section, subjects in obj.marks.items():
            html += f"<strong>{section}</strong><br>"
            for sub_name, mark in subjects.items():
                html += f"{sub_name}: {mark}<br>"
            html += "<hr>"
        return format_html(html)

    show_marks.short_description = "Marks"


class CenterForm(forms.ModelForm):
    class Meta:
        model = Center
        fields = ['name', 'code', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Center Name'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Center Code'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Center Address', 'rows':3}),
        }