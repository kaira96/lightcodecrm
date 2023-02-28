from django.contrib import admin
from .models import Role, Employee, Student, Expense, Income, Currency, PaymentMethod, Lead, Course, StudyingTime, LearningFormat


class RoleAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_date']


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'role', 'is_active']
    list_filter = ('created_date', 'studying_time', 'format', 'course', 'role', 'is_active')
    search_fields = ['full_name', 'role']


class StudentAdmin(admin.ModelAdmin):
    readonly_fields = ('last_payment_date', )
    list_display = [
        'full_name',
        'course',
        'teacher',
        'studying_time',
        'format',
        'certificate',
        'is_graduate',
        'created_date',
        'total_payment',
        'last_payment_date']
    list_filter = ('created_date', 'course', 'is_graduate')
    search_fields = ['full_name', 'phone_number']


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['title', 'value', 'flow_type', 'created_date']
    list_filter = ('flow_type', 'created_date')
    search_fields = ['title', ]


class IncomeAdmin(admin.ModelAdmin):
    list_display = ['student', 'payment_method', 'value', 'currency', 'date_of_payment', 'created_date']
    list_filter = (
        'created_date',
        'student__course',
        'payment_method',
        'student__format',
        'student__studying_time',
        'student__teacher')
    search_fields = ['student', ]


class LeadAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'created_date', 'is_add']
    list_filter = ('created_date', 'is_add')
    search_fields = ['full_name', 'phone_number']


class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_date', 'is_active']
    list_filter = ('created_date', 'is_active')


admin.site.register(Role, RoleAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Income, IncomeAdmin)
admin.site.register(Currency)
admin.site.register(PaymentMethod)
admin.site.register(Lead, LeadAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(StudyingTime)
admin.site.register(LearningFormat)



