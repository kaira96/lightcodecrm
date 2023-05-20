from django.contrib import admin
from django import forms
from modeltranslation.admin import TranslationAdmin
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import CourseForLanding, Review, StudyingTime, Article, Section, SubscriptionToCourse, Stream


class ArticleAdminForm(forms.ModelForm):
    body_ru = forms.CharField(label='Контент [ru]', widget=CKEditorUploadingWidget())
    body_ky = forms.CharField(label='Контент [ky]', widget=CKEditorUploadingWidget(), required=False)


class StudyingTimeAdmin(TranslationAdmin):
    list_display = ['title']


class CourseAdmin(TranslationAdmin):
    list_display = ['title', 'studying_time_names', 'teacher', 'format_names', 'created_date', 'is_active']
    list_filter = ('studying_time', 'format', 'created_date', 'is_active')
    prepopulated_fields = {'slug': ('title',)}


class ArticleAdmin(TranslationAdmin):
    list_display = ['teacher', 'topic_name', 'section', 'created_date']
    prepopulated_fields = {'slug': ('topic_name',)}
    list_filter = ('created_date', )
    form = ArticleAdminForm


class SectionAdmin(TranslationAdmin):
    prepopulated_fields = {'slug': ('title',)}


class SubscriptionToCourseAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'created_date']
    list_filter = ('course', 'created_date')


admin.site.register(CourseForLanding, CourseAdmin)
admin.site.register(Review)
admin.site.register(StudyingTime, StudyingTimeAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(SubscriptionToCourse, SubscriptionToCourseAdmin)
admin.site.register(Stream)
