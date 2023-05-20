from modeltranslation.translator import register, TranslationOptions
from ckeditor.fields import RichTextField
from .models import StudyingTime, CourseForLanding, Review, Section, Article


@register(StudyingTime)
class StudyingTimeTranslationOptions(TranslationOptions):
    fields = ('title', )


@register(CourseForLanding)
class CourseForLandingTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'additional_info')


@register(Review)
class ReviewTranslationOptions(TranslationOptions):
    fields = ('name', 'direction', 'description')


@register(Section)
class SectionTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(Article)
class ArticleTranslationOptions(TranslationOptions):
    body = RichTextField()
    fields = ('topic_name', 'body')
    widgets = {
        'body': RichTextField,
    }




