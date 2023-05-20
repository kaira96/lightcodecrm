from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.urls import reverse
from srm.models import Employee, Lead
from account.models import MyUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import messages
from classroom.models import Student, Teacher, Classroom
from classroom.forms import UserRegistrationForm, UserAuthenticationForm
from .forms import SectionForm, ArticleForm, StreamForm
from .models import CourseForLanding, Review, Section, Article, SubscriptionToCourse, Stream
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
        messages.error(request, 'Повторите попытку, убедитесь что поля заполнены в правильном формате')
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
    is_creator = Article.objects.filter(teacher=request.user, section=section).exists()
    if request.method == 'POST':
        SubscriptionToCourse.objects.create(user=request.user, course=section)
        return redirect('tutorial-content', section.slug)
    return render(request, template_name='landing/tutorial_content.html', context={
        'articles': articles,
        'section': section,
        'is_subscribed': is_subscribed,
        'is_creator': is_creator})


@login_required(login_url='/registration/')
def content_view(request, slug):
    article = Article.objects.get(slug=slug)
    articles = Article.objects.filter(section=article.section)
    is_subscribed = SubscriptionToCourse.objects.filter(user=request.user, course=article.section).exists()
    is_creator = Article.objects.filter(teacher=request.user, section=article.section).exists()
    if not is_subscribed and not is_creator:
        return redirect('content_view', article.slug)
    if request.method == 'POST':
        SubscriptionToCourse.objects.create(user=request.user, course=article.section)
        return redirect('content_view', article.slug)
    return render(request, template_name='landing/content-detail.html', context={
        'article': article,
        'articles': articles,
        'is_subscribed': is_subscribed})


@user_passes_test(lambda u: u.is_admin or u.status == 4, login_url='/registration/')
def add_category(request):
    if request.method == 'POST':
        form = SectionForm(data=request.POST)
        if form.is_valid():
            section = form.save()
            if request.POST['is_next'] == 'on':
                return redirect('add_category')
            return redirect('tutorials')
        messages.error(request, 'Повторите попытку, убедитесь что поля заполнены в правильном формате')
    form = SectionForm()
    return render(request, template_name='landing/add-category.html', context={'form': form})


@user_passes_test(lambda u: u.is_admin or u.status == 4, login_url='/registration/')
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
        messages.error(request, 'Повторите попытку, убедитесь что поля заполнены в правильном формате')
    form = ArticleForm()
    return render(request, template_name='landing/add-article.html', context={'form': form})


def register_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user_phone_number = form.cleaned_data.get('phone_number')
            login(request, user)
            return redirect('index')
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
                return redirect('index')
            else:
                messages.error(request, 'Неверный номер телефона или пароль')
                return render(request, 'landing/authentication.html', {'form': form})
    form = UserAuthenticationForm()
    return render(request, 'landing/authentication.html', {'form': form})


@user_passes_test(lambda u: u.is_admin or u.status == 4, login_url='/registration/')
def add_url_stream(request):
    if request.method == 'POST':
        form = StreamForm(data=request.POST)
        if form.is_valid():
            url = form.save()
            return redirect('index')
        messages.error(request, 'Повторите попытку, убедитесь что поля заполнены в правильном формате')
    form = StreamForm()
    return render(request, template_name='landing/add_url_stream.html', context={'form': form})


def error_404(request, exception):
    return render(request, 'landing/404error.html')


def error_500(request):
    return render(request, 'landing/500error.html')


@login_required(login_url='/registration/')
def logout_view(request):
    logout(request)
    return redirect('index')


@login_required(login_url='/registration/')
@user_passes_test(lambda u: u.is_admin or u.status == 4, login_url='/registration/')
def article_list(request):
    articles = Article.objects.filter(teacher=request.user.id).order_by('-id')
    return render(request, template_name='landing/list_articles.html', context={'articles': articles})


@user_passes_test(lambda u: u.is_admin or u.status == 4, login_url='/registration/')
def article_detail(request, pk):
    article = get_object_or_404(Article, id=pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('tutorials')
        messages.error(request, 'Повторите попытку, убедитесь что поля заполнены в правильном формате')
    else:
        form = ArticleForm(instance=article)

    return render(request, template_name='landing/article_detail.html', context={'article': article, 'form': form})


@user_passes_test(lambda u: u.is_admin or u.status == 4, login_url='/registration/')
def article_delete(request, pk):

    article = Article.objects.get(id=pk)
    article.delete()

    return HttpResponseRedirect(reverse('article_list'))


