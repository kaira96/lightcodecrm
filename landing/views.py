from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import CourseForLanding, Review, Section, Article, SubscriptionToCourse, Stream
from srm.models import Employee, Lead
from account.models import MyUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import messages
from classroom.models import Student, Teacher, Classroom
from classroom.forms import UserRegistrationForm, UserAuthenticationForm
from .forms import SectionForm, ArticleForm, StreamForm
from django.utils import timezone
now = timezone.now()


def index(request):
    courses = CourseForLanding.objects.all()
    reviews = Review.objects.all()
    employees = Employee.objects.filter(is_active=True)
    stream = Stream.objects.filter(is_active=True, start_time__lte=now, end_time__gte=now).last()
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
        'employees': employees,
        'stream': stream})


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


@login_required(login_url='/registration/')
def personal_area(request):
    user = MyUser.objects.get(id=request.user.id)
    students = Student.objects.filter(student=request.user.id)
    sections = SubscriptionToCourse.objects.filter(user=request.user)
    subscriptions = SubscriptionToCourse.objects.filter(user=request.user)
    classrooms = Classroom.objects.filter(student__student=request.user).distinct()
    mentors = {}
    for classroom in classrooms:
        teacher = classroom.teacher_set.first().teacher
        mentors[classroom.id] = teacher
    return render(request, template_name='landing/personal_area.html', context={
        'user': user,
        'students': students,
        'sections': sections,
        'subscriptions': subscriptions,
        'mentors': 'mentors'
    })


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


@login_required(login_url='/registration/')
def theme_view(request, slug):
    section = Section.objects.get(slug=slug)
    articles = Article.objects.filter(section=section)
    is_subscribed = SubscriptionToCourse.objects.filter(user=request.user, course=section).exists()
    if request.method == 'POST':
        SubscriptionToCourse.objects.create(user=request.user, course=section)
        return redirect('tutorial-content', section.slug)
    return render(request, template_name='landing/tutorial_content.html', context={
        'articles': articles,
        'section': section,
        'is_subscribed': is_subscribed})


@login_required(login_url='/registration/')
def content_view(request, slug):
    article = Article.objects.get(slug=slug)
    articles = Article.objects.filter(section=article.section)
    is_subscribed = SubscriptionToCourse.objects.filter(user=request.user, course=article.section).exists()
    if not is_subscribed:
        return redirect('tutorial-content', article.section.slug)
    return render(request, template_name='landing/content-detail.html', context={'article': article, 'articles': articles})


@user_passes_test(lambda u: u.is_superuser or u.status == 4, login_url='/registration/')
def add_category(request):
    if request.method == 'POST':
        form = SectionForm(data=request.POST)
        if form.is_valid():
            section = form.save()
            if request.POST['is_next'] == 'on':
                return redirect('add_category')
            return redirect('tutorials')
    messages.error(request, 'Заполните поля в правильном формате.')
    form = SectionForm()
    return render(request, template_name='landing/add-category.html', context={'form': form})


@user_passes_test(lambda u: u.is_superuser or u.status == 4, login_url='/register/')
def add_article(request):
    if request.method == 'POST':
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.teacher = MyUser.objects.get(id=request.user.id)
            obj.save()
            if request.POST['is_next'] == 'on':
                return redirect('add_article')
            return redirect('tutorials')
    messages.error(request, 'Заполните поля в правильном формате.')
    form = ArticleForm()
    return render(request, template_name='landing/add-article.html', context={'form': form})


def register_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user_phone_number = form.cleaned_data.get('phone_number')
            login(request, user)
            return redirect('tutorials')
        else:
            return render(request, 'landing/registration.html', {'form': form})
    form = UserRegistrationForm()
    return render(request, 'landing/registration.html', {'form': form})


def authentication_view(request):
    if request.method == "POST":
        form = UserAuthenticationForm(data=request.POST)
        if form.is_valid():
            user_phone_number = form.cleaned_data.get('phone_number')
            password = form.cleaned_data.get('password')
            user = authenticate(username=user_phone_number, password=password)
            if user != None:
                login(request, user)
                return redirect('tutorials')
        else:
            messages.success(request, 'Неправильный пароль')
            return render(request, 'landing/authentication.html', {'form': form})
    form = UserAuthenticationForm()
    return render(request, 'landing/authentication.html', {'form': form})


@user_passes_test(lambda u: u.is_superuser or u.status == 4, login_url='/registration/')
def add_url_stream(request):
    if request.method == 'POST':
        form = StreamForm(data=request.POST)
        if form.is_valid():
            url = form.save()
            return redirect('index')
    messages.error(request, 'Заполните поля в правильном формате.')
    form = StreamForm()
    return render(request, template_name='landing/add_url_stream.html', context={'form': form})


