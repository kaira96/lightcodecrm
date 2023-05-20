from django import forms
from .models import Question, Comment, AccessRights
from account.models import MyUser
from django_select2 import forms as s2forms


class UserWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "username__iregex",
    ]


class QuestionCreateForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ['title', 'body']


class CommentCreateForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['body', 'parent_comment']


class AccessRightsForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=MyUser.objects.exclude(id__in=AccessRights.objects.values_list('user_id', flat=True)),
        widget=UserWidget,
        label='Пользователь'
    )
    end_date = forms.DateField(widget=forms.widgets.DateInput(
        attrs={'type': 'date'}),
        label='Конец даты',
        required=False)

    is_ban_forever = forms.BooleanField(required=False, label='Забанить навсегда')

    class Meta:
        model = AccessRights
        fields = ['user', 'is_ban_forever', 'end_date']


