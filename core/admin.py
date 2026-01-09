from django.contrib import admin
from .models import Marksheet

class MarksheetAdmin(admin.ModelAdmin):
    list_display = ('student', 'show_marks', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('student__name', 'student__roll_no')

    def show_marks(self, obj):
        output = ""
        for sec, subs in obj.theory_marks.items():
            output += f"Theory - {sec}: {subs.get('obtained')}<br>"
        for sec, subs in obj.practical_marks.items():
            output += f"Practical - {sec}: {subs.get('obtained')}<br>"
        return output

    show_marks.allow_tags = True
    show_marks.short_description = "Marks Summary"
