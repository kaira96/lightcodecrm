import re

from django import forms
from .models import Section, Article, Stream
from ckeditor.widgets import CKEditorWidget
from django_select2 import forms as s2forms


class SectionWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "title__iregex",
    ]


class SectionForm(forms.ModelForm):

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        if not re.match(r'^[-a-zA-Z0-9_/\\|#.+]+$', slug):
            raise forms.ValidationError('Invalid slug')
        return slug

    id_section = forms.ModelChoiceField(
        queryset=Section.objects.all(),
        widget=SectionWidget,
        required=False
    )

    class Meta:
        model = Section
        fields = ['title', 'slug', 'id_section', 'description']


class ArticleForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorWidget())
    # body_ky = forms.CharField(widget=CKEditorWidget(), label='На кыргызском (Не обязательное)', required=False)
    section = forms.ModelChoiceField(
        queryset=Section.objects.all(),
        widget=SectionWidget,
        label='Раздел'
    )

    class Meta:
        model = Article
        fields = ['topic_name', 'slug', 'section', 'body']


class StreamForm(forms.ModelForm):
    start_time = forms.DateTimeField(widget=forms.widgets.DateTimeInput(
        attrs={'type': 'datetime-local', 'placeholder': 'yyyy-mm-dd (DOB)', 'class': 'form-control'}))
    end_time = forms.DateTimeField(widget=forms.widgets.DateTimeInput(
        attrs={'type': 'datetime-local', 'placeholder': 'yyyy-mm-dd (DOB)', 'class': 'form-control'}))

    class Meta:
        model = Stream
        fields = ['url', 'start_time', 'end_time', 'is_active']


