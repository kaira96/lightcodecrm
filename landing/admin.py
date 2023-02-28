from django.contrib import admin
from .models import CourseForLanding, Review, StudyingTime, Tutorial, Article, Section


class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'studying_time_names', 'teacher', 'format_names', 'created_date', 'is_active']
    list_filter = ('studying_time', 'format', 'created_date', 'is_active')
    prepopulated_fields = {'slug': ('title',)}


class TutorialAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'created_date']


admin.site.register(CourseForLanding, CourseAdmin)
admin.site.register(Review)
admin.site.register(StudyingTime)
admin.site.register(Tutorial, TutorialAdmin)
admin.site.register(Article)
admin.site.register(Section)
