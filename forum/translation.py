from modeltranslation.translator import register, TranslationOptions
from .models import Topic, Question, Comment


@register(Topic)
class TopicTranslationOptions(TranslationOptions):
    fields = ('title', )


@register(Question)
class QuestionTranslationOptions(TranslationOptions):
    fields = ('title', 'body')


@register(Comment)
class CommentTranslationOptions(TranslationOptions):
    fields = ('body', )


