import django_filters
from django_filters import DateFromToRangeFilter
from django import forms
from django_select2 import forms as s2forms

from .models import Income, Expense, Student, Course, Lead


class RangeWidget(forms.MultiWidget):

    def __init__(self, attrs=None):
        def get_widget_attrs(override=None):
            widget_attrs = {
                'type': 'date',
                'placeholder': 'yyyy-mm-dd (DOB)',
                'class': 'form-control',
            }
            if override:
                widget_attrs.update(override)
            return widget_attrs

        widgets = (
            forms.TextInput(attrs=get_widget_attrs({'type': 'date'})),
            forms.TextInput(attrs=get_widget_attrs()),
        )
        super(RangeWidget, self).__init__(widgets, attrs)


class StudentWidget(s2forms.ModelSelect2Widget):
    model = Student
    search_fields = [
        "full_name__iregex",
    ]


class LeadWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "phone_number__icontains"
    ]


class DateRangeWidget(forms.widgets.MultiWidget):
    def __init__(self, attrs=None):
        widgets = (
            forms.widgets.DateInput(attrs={"type": "date"}),
            forms.widgets.DateInput(attrs={"type": "date"}),
        )
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return value.split(',')
        return ['', '']


class CustomDateInput(forms.DateInput):
    input_type = 'date'
    format = '%Y-%m-%d'
    attrs = {'class': 'form-control'}


class IncomeFilter(django_filters.FilterSet):
    created_date = DateFromToRangeFilter(
        field_name='created_date',
        widget=DateRangeWidget(attrs={'class': 'form-control'})
    )
    student = django_filters.ModelChoiceFilter(
        queryset=Student.objects.all(),
        widget=StudentWidget,
    )
    student__course__title = django_filters.ModelChoiceFilter(
        queryset=Course.objects.all()
    )

    class Meta:
        model = Income
        fields = [
            'created_date',
            'student',
            'student__course',
            'payment_method',
            'student__format',
            'student__studying_time',
            'student__teacher',
            'currency']


class ExpenseFilter(django_filters.FilterSet):
    # created_date = DateFromToRangeFilter(field_name='created_date', widget=RangeWidget(
    #     attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)', 'class': 'form-control'}))
    # created_date = DateFromToRangeFilter(field_name='created_date')
    created_date = DateFromToRangeFilter(
        field_name='created_date',
        widget=DateRangeWidget(attrs={'class': 'form-control', 'id': "start_date"})
    )

    class Meta:
        model = Expense
        fields = ['flow_type', 'created_date']


class StudentFilter(django_filters.FilterSet):
    # created_date = DateFromToRangeFilter(field_name='created_date', widget=RangeWidget(
    #     attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)', 'class': 'form-control'}))
    # created_date = DateFromToRangeFilter(field_name='created_date', widget=RangeWidget())
    created_date = DateFromToRangeFilter(
        field_name='created_date',
        widget=DateRangeWidget(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Student
        fields = [
            'course',
            'is_graduate',
            'studying_time',
            'format',
            'teacher',
            'created_date']


class LeadFilter(django_filters.FilterSet):
    created_date = DateFromToRangeFilter(
        field_name='created_date',
        widget=DateRangeWidget(attrs={'class': 'form-control'})
    )
    full_name = django_filters.ModelChoiceFilter(
        queryset=Lead.objects.all(),
        widget=StudentWidget
    )
    phone_number = django_filters.ModelChoiceFilter(
        queryset=Lead.objects.all(),
        widget=LeadWidget
    )

    class Meta:
        model = Lead
        fields = ['full_name', 'phone_number', 'created_date']

