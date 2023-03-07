from django import forms
from .models import Section, Article, Stream
from ckeditor.widgets import CKEditorWidget


class SectionForm(forms.ModelForm):

    class Meta:
        model = Section
        fields = ['title', 'slug', 'id_section']


class ArticleForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorWidget())

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


