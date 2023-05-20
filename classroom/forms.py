from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from account.models import MyUser
from datetime import datetime
from .models import Student
from django_select2 import forms as s2forms


class UserRegistrationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['phone_number'].label = ''
        self.fields['username'].label = ''
        self.fields['password1'].label = ''
        self.fields['password2'].label = ''
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Номер телефона (+996)'
        self.fields['username'].widget.attrs['placeholder'] = 'Имя пользователя'
        self.fields['password1'].widget.attrs['placeholder'] = 'Пароль'
        self.fields['password2'].widget.attrs['placeholder'] = 'Повторно введите пароль'

    password1 = forms.CharField(label='Введите паорль',
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтвердите пароль',
                                widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ("phone_number", "username", "password1", "password2")


class UserAuthenticationForm(forms.Form):
    phone_number = forms.CharField(label='Введите номер телефона',
                                   widget=forms.TextInput(attrs={'placeholder': '+996'}))

    password = forms.CharField(label='Введите пароль',
                               widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ("phone_number", "password")


class CreateAssignmentForm(forms.Form):

    assignment_name = forms.CharField(max_length=50, label='Название задания')
    due_date = forms.DateField(initial=datetime.now().date(), label='Срок сдачи')
    due_time = forms.TimeField(initial=datetime.now().time(), label='Время сдачи')
    instructions = forms.CharField(label='Инструкция', widget=forms.Textarea)
    total_marks = forms.IntegerField(label='Максимальное количество баллов')


class CreateClassForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(CreateClassForm,self).__init__()
        self.fields['class_name'].label = ''
        self.fields['section'].label = ''
        self.fields['class_name'].widget.attrs['placeholder'] = 'Название класса'
        self.fields['section'].widget.attrs['placeholder'] = 'Раздел'


class JoinClassForm(forms.Form):
    code = forms.CharField(max_length=10, label='code')


class SubmitAssignmentForm(forms.Form):
    submission_file = forms.FileField(label='Файл')


class StudentsWidget(s2forms.ModelSelect2Widget):
    model = Student
    search_fields = [
        "username__iregex",
    ]


class StudentAddForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        classroom = kwargs.pop('classroom', None)
        print('classroom:', classroom)
        super().__init__(*args, **kwargs)
        if classroom:
            self.fields['student'].queryset = MyUser.objects.exclude(
                id__in=Student.objects.filter(classroom=classroom).values_list('student_id'))
        print('queryset:', self.fields['student'].queryset)

    student = forms.ModelChoiceField(
        queryset=MyUser.objects.all(),
        widget=StudentsWidget
    )

    class Meta:
        model = Student
        fields = ['student']




