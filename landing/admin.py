from django.contrib import admin
from .models import CourseForLanding, Review, StudyingTime, Article, Section


class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'studying_time_names', 'teacher', 'format_names', 'created_date', 'is_active']
    list_filter = ('studying_time', 'format', 'created_date', 'is_active')
    prepopulated_fields = {'slug': ('title',)}


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'section',]
    list_filter = ('created_date', )


class SectionAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(CourseForLanding, CourseAdmin)
admin.site.register(Review)
admin.site.register(StudyingTime)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Section, SectionAdmin)
