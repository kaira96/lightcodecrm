from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import Classroom, Student, Teacher, Assignment, Submission


class ClassroomAdmin(TranslationAdmin):
    list_display = ['classroom_name', 'section', 'created_date']
    list_filter = ('section', 'created_date')


class StudentAdmin(admin.ModelAdmin):
    list_display = ['student', 'classroom', 'created_date']
    list_filter = ('created_date', 'classroom__classroom_name')


class TeacherAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'classroom', 'created_date']
    list_filter = ('created_date', 'classroom__classroom_name')


class AssignmentAdmin(TranslationAdmin):
    list_display = ['assignment_name', 'classroom', 'posted_date']
    list_filter = ('classroom__classroom_name', 'posted_date')


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['student', 'assignment', 'submitted_date']
    list_filter = ('submitted_date', )


admin.site.register(Classroom, ClassroomAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(Submission, SubmissionAdmin)


