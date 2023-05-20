from modeltranslation.translator import register, TranslationOptions
from .models import Classroom, Assignment


@register(Classroom)
class ClassroomTranslationOptions(TranslationOptions):
    fields = ('classroom_name', 'section')


@register(Assignment)
class AssignmentTranslationOptions(TranslationOptions):
    fields = ('assignment_name', 'instruction')


