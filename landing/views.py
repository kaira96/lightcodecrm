from django.shortcuts import render
from .models import CourseForLanding, Review, Section
from srm.models import Employee, Lead
from account.models import MyUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import messages
from classroom.models import Student, Teacher


def index(request):
    courses = CourseForLanding.objects.all()
    reviews = Review.objects.all()
    employees = Employee.objects.filter(is_active=True)
    print(reviews)
    if request.method == 'POST':
        if request.POST.get('name'):
            user_name = request.POST.get('name')
            user_phone_number = request.POST.get('phone_number')

            Lead.objects.create(
                full_name=user_name,
                phone_number=user_phone_number
            )
        elif request.POST.get('email'):
            user_email = request.POST.get('email')
            user_password = request.POST.get('password')

            if MyUser.objects.filter(email=user_email).exists():
                messages.error(request, 'Пользователь с такой почтой уже существует.')
            else:
                MyUser.objects.create_user(email=user_email, password=user_password)
    return render(request, template_name='landing/index.html', context={
        'courses': courses,
        'reviews': reviews,
        'employees': employees})


@receiver(post_save, sender=Lead)
def remove_from_inventory(sender, **kwargs):
    Lead.objects.filter(is_add=True).delete()


def course_detail(request, slug):

    course = CourseForLanding.objects.get(slug=slug)

    return render(request, template_name='landing/course-detail.html', context={'course': course})


def employee_detail(request, pk):
    employee = Employee.objects.get(pk=pk)
    course = CourseForLanding.objects.filter(teacher=employee)
    return render(request, template_name='landing/employee.html', context={'employee': employee, 'courses': course})


def personal_area(request):
    user = MyUser.objects.get(id=request.user.id)
    students = Student.objects.filter(student=request.user.id)
    tt = Teacher.objects.filter()
    return render(request, template_name='landing/personal_area.html', context={'user': user, 'students': students})


def category_view(request, slug=None):

    if slug is None:
        sections = Section.objects.filter(id_section=None)
    else:
        sections = Section.objects.get(slug=slug).children.all()

    return render(request, template_name='landing/tutorials.html', context={'sections': sections})


def category_detail(request, slug):
    section = Section.objects.get(slug=slug)
    sections = Section.objects.get(slug=slug).children.all()
    return render(request, template_name='landing/category-detail.html', context={'sections': sections, 'section': section})


def theme_view(request):
    ...
