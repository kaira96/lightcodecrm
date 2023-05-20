from django.contrib import admin
from .models import Topic, Question, Comment, AccessRights
from modeltranslation.admin import TranslationAdmin


class TopicAdmin(TranslationAdmin):
    list_display = ['title', 'created_date']
    list_filter = ('created_date', )
    prepopulated_fields = {'slug': ('title',)}


class QuestionAdmin(TranslationAdmin):
    list_display = ['user', 'topic', 'title', 'created_date']
    list_filter = ('topic', 'created_date')
    search_fields = ['topic', 'user']


class CommentAdmin(TranslationAdmin):
    ...


class AccessRightsAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_date', 'end_date', 'created_date']
    list_filter = ('created_date', 'end_date')
    search_fields = ['user']


admin.site.register(Topic, TopicAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(AccessRights, AccessRightsAdmin)
