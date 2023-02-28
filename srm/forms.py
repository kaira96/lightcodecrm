from django import forms
from .models import Lead, Student, Income, Expense, Course, Employee
from django_select2 import forms as s2forms


class StudentWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "full_name__iregex",
    ]


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['full_name', 'phone_number', 'course', 'is_add', 'description']


# class AppointmentUpdateForm(forms.ModelForm):
#
#     class Meta:
#         model = Appointment
#         fields = ('status', 'assignment_start_date', 'assignment_end_date', 'more_information', 'services')
#         widgets = {
#             'assignment_start_date': forms.widgets.DateTimeInput(
#                 attrs={'type': 'datetime-local'},
#                 format='%Y-%m-%d %H:%M'
#             ),
#             'assignment_end_date': forms.widgets.DateTimeInput(
#                 attrs={'type': 'datetime-local'},
#                 format='%Y-%m-%d %H:%M'),
#         }
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['services'].queryset = self.fields['services'].queryset.filter(
#             company=kwargs['instance'].company_branch.company
#         )

class CustomSelectWidget(forms.Select):
    def create_option(self, name, value, *args, **kwargs):
        option = super().create_option(name, value, *args, **kwargs)
        if value:
            option['attrs']['data-courses'] = value.instance.course_names  # set option attribute
            option['attrs']['data-studying_time'] = value.instance.studying_time_names  # set option attribute
            option['attrs']['data-format'] = value.instance.format_names  # set option attribute
        return option


class StudentForm(forms.ModelForm):
    last_payment_date = forms.DateField(widget=forms.widgets.DateInput(
        attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)', 'class': 'form-control'}),
        required=False
    )
    remainder = forms.DecimalField(label='Общая оплата за курс')
    teacher = forms.ModelChoiceField(
        queryset=Employee.objects.all(),
        widget=CustomSelectWidget
    )

    class Meta:
        model = Student
        fields = ['full_name', 'phone_number', 'course', 'teacher', 'studying_time', 'format', 'certificate', 'url', 'is_graduate', 'remainder', 'description']


class IncomeForm(forms.ModelForm):
    student = forms.ModelChoiceField(
        queryset=Student.objects.all(),
        widget=StudentWidget
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
    class Meta:
        model = Expense
        fields = ['title', 'value', 'flow_type']
