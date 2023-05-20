from django import forms
from .models import Lead, Student, Income, Expense, Course, Employee
from django_select2 import forms as s2forms


class StudentWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "full_name__iregex",
    ]


class TeacherWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "full_name__iregex",
    ]


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['full_name', 'phone_number', 'course', 'is_add', 'description']


class StudentForm(forms.ModelForm):
    last_payment_date = forms.DateField(widget=forms.widgets.DateInput(
        attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)', 'class': 'form-control'}),
        required=False,
        label='Дата последней оплаты'
    )
    remainder = forms.DecimalField(label='Общая оплата за курс')
    teacher = forms.ModelChoiceField(
        queryset=Employee.objects.all(),
        widget=TeacherWidget,
        label='Ментор'
    )

    class Meta:
        model = Student
        fields = ['full_name', 'phone_number', 'course', 'teacher', 'studying_time', 'format', 'certificate', 'url', 'is_graduate', 'remainder', 'description']


class IncomeForm(forms.ModelForm):
    student = forms.ModelChoiceField(
        queryset=Student.objects.all(),
        widget=StudentWidget,
        label='Студент'
    )
    date_of_payment = forms.DateField(widget=forms.widgets.DateInput(
        attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)', 'class': 'form-control'}),
        label='Дата оплаты'
    )

    class Meta:
        model = Income
        fields = ['student', 'value', 'payment_method', 'currency', 'date_of_payment']
        # widgets = {
        #     "student": StudentWidget,
        # }


class ExpenseForm(forms.ModelForm):
    date_of_payment = forms.DateField(widget=forms.widgets.DateInput(
        attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)', 'class': 'form-control'}),
        label='Дата'
    )

    class Meta:
        model = Expense
        fields = ['title', 'value', 'flow_type', 'date_of_payment']
