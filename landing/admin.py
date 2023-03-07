from django.contrib import admin
from .models import CourseForLanding, Review, StudyingTime, Article, Section, SubscriptionToCourse, Stream


class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'studying_time_names', 'teacher', 'format_names', 'created_date', 'is_active']
    list_filter = ('studying_time', 'format', 'created_date', 'is_active')
    prepopulated_fields = {'slug': ('title',)}


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'topic_name', 'section', 'created_date']
    prepopulated_fields = {'slug': ('topic_name',)}
    list_filter = ('created_date', )


class SectionAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class SubscriptionToCourseAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'created_date']
    list_filter = ('course', 'created_date')


admin.site.register(CourseForLanding, CourseAdmin)
admin.site.register(Review)
admin.site.register(StudyingTime)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(SubscriptionToCourse, SubscriptionToCourseAdmin)
admin.site.register(Stream)
