from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.http import JsonResponse
from itertools import chain
from django.contrib import messages
from django.utils.timesince import timesince
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

from .decorators import login_excluded, student_required, access_class, teacher_required, student_required
from .forms import UserAuthenticationForm, UserRegistrationForm, CreateAssignmentForm, SubmitAssignmentForm,\
    StudentAddForm
from .models import Student, Teacher, Classroom, Assignment, Submission
from .utils import generate_class_code
from account.models import MyUser


# home -->
def landing_page(request):
    return render(request, 'classroom/landing.html')


@login_required(login_url='login')
def home(request):
    teacher_mapping = Teacher.objects.filter(teacher=request.user).select_related('classroom')
    student_mapping = Student.objects.filter(student=request.user).select_related('classroom')
    teachers_all = Teacher.objects.all()
    mappings = chain(teacher_mapping, student_mapping)
    return render(request, 'classroom/home.html', {'mappings': mappings, 'teachers_all': teachers_all})


# auth -->
@login_excluded('home')
def register_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user_phone_number = form.cleaned_data.get('phone_number')
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'classroom/register.html', {'form': form})
    form = UserRegistrationForm()
    return render(request, 'classroom/register.html', {'form': form})


@login_excluded('home')
def login_view(request):
    if request.method == "POST":
        form = UserAuthenticationForm(data=request.POST)
        if form.is_valid():
            user_phone_number = form.cleaned_data.get('phone_number')
            password = form.cleaned_data.get('password')
            user = authenticate(username=user_phone_number, password=password)
            if user != None:
                login(request, user)
                return redirect('home')
        else:
            messages.success(request, 'Неправильный пароль')
            return render(request, 'classroom/login.html', {'form': form})
    form = UserAuthenticationForm()
    return render(request, 'classroom/login.html', {'form': form})


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')


# class -->
@login_required(login_url='login')
@student_required('home')
def unenroll_class(request, classroom_id):
    classroom = Classroom.objects.get(pk=classroom_id)
    student_mapping = Student.objects.filter(student=request.user, classroom=classroom).delete()
    return redirect('home')


@login_required(login_url='login')
# @teacher_required('home')
def delete_class(request, classroom_id):
    classroom = Classroom.objects.get(pk=classroom_id)
    teacher_mapping = Teacher.objects.get(teacher=request.user, classroom=classroom)
    teacher_mapping.delete()
    classroom.delete()
    return redirect('home')


@login_required(login_url='login')
@access_class('home')
def render_class(request, id):
    classroom = Classroom.objects.get(pk=id)
    try:
        assignments = Assignment.objects.filter(classroom=id)
    except Exception as e:
        assignments = None

    try:
        students = Student.objects.filter(classroom=id)
    except Exception as e:
        students = None
    teachers = Teacher.objects.filter(classroom=id)

    teacher_mapping = Teacher.objects.filter(teacher=request.user).select_related('classroom')
    student_mapping = Student.objects.filter(student=request.user).select_related('classroom')
    mappings = chain(teacher_mapping, student_mapping)
    return render(request, 'classroom/class_page.html',
                  {'classroom': classroom, 'assignments': assignments, 'students': students, 'teachers': teachers,
                   "mappings": mappings})


@login_required(login_url='login')
def create_class_request(request):
    if request.POST.get('action') == 'post':
        classrooms = Classroom.objects.all()
        existing_codes = []
        for classroom in classrooms:
            existing_codes.append(classroom.class_code)

        class_name = request.POST.get('class_name')
        section = request.POST.get('section')

        class_code = generate_class_code(6, existing_codes)
        classroom = Classroom(classroom_name=class_name, section=section, class_code=class_code)
        classroom.save()
        teacher = Teacher(teacher=request.user, classroom=classroom)
        teacher.save()
        return JsonResponse({'status': 'SUCCESS'})


@login_required(login_url='login')
def join_class_request(request):
    if request.POST.get('action') == 'post':
        code = request.POST.get('class_code')
        try:
            classroom = Classroom.objects.get(class_code=code)
            student = Student.objects.filter(student=request.user, classroom=classroom)
            if (student.count() != 0):
                return redirect('home')
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'FAIL', 'message': str(e)})
        student = Student(student=request.user, classroom=classroom)
        student.save()
        return JsonResponse({'status': 'SUCCESS'})


# assignments -->
@login_required(login_url='login')
# @teacher_required('home')
def create_assignment(request, classroom_id):
    teacher_mapping = Teacher.objects.filter(teacher=request.user).select_related('classroom')
    student_mapping = Student.objects.filter(student=request.user).select_related('classroom')
    mappings = chain(teacher_mapping, student_mapping)

    if request.method == 'POST':
        form = CreateAssignmentForm(request.POST)
        if form.is_valid():
            assignment_name = form.cleaned_data.get('assignment_name')
            due_date = form.cleaned_data.get('due_date')
            due_time = form.cleaned_data.get('due_time')
            classroom = Classroom.objects.get(pk=classroom_id)
            instructions = form.cleaned_data.get('instructions')
            total_marks = form.cleaned_data.get('total_marks')
            assignment = Assignment(assignment_name=assignment_name, due_date=due_date, due_time=due_time,
                                     instruction=instructions, total_marks=total_marks, classroom=classroom)
            assignment.save()
            return redirect('render_class', id=classroom.id)
        else:
            return render(request, 'classroom/create_assignment.html', {'form': form, 'mappings': mappings})
    form = CreateAssignmentForm()
    return render(request, 'classroom/create_assignment.html', {'form': form, 'mappings': mappings})


@login_required(login_url='login')
# @teacher_required('home')
def assignment_summary(request, assignment_id):
    assignment = Assignment.objects.filter(pk=assignment_id).first()
    submissions = Submission.objects.filter(assignment=assignment)
    teachers = Teacher.objects.filter(classroom=assignment.classroom)
    teacher_mapping = Teacher.objects.filter(teacher=request.user).select_related('classroom')
    student_mapping = Student.objects.filter(student=request.user).select_related('classroom')
    no_of_students = Student.objects.filter(classroom=assignment.classroom)
    mappings = chain(teacher_mapping, student_mapping)
    print(request.POST)
    mark = request.POST.get('submission_marks')
    return render(request, 'classroom/assignment_summary.html',
                  {'assignment': assignment, 'submissions': submissions, 'mappings': mappings,
                   'no_of_students': no_of_students})


@login_required(login_url='login')
# @teacher_required('home')
def delete_assignment(request, assignment_id):
    try:
        assignment = Assignment.objects.get(pk=assignment_id)
        classroom = assignment.classroom.id
        Assignment.objects.get(pk=assignment_id).delete()
        return redirect('render_class', id=classroom)
    except Exception as e:
        print(str(e))
        return redirect('home')


# submission -->
# @csrf_exempt
# @login_required(login_url='login')
# # @student_required('home')
# def submit_assignment_request(request, assignment_id):
#     assignment = Assignment.objects.get(pk=assignment_id)
#     student = Student.objects.get(classroom=assignment.classroom, student=request.user.id)
#     file_name = request.POST.get('my')
#     print(request.POST)
#
#     try:
#         submission = Submission.objects.get(assignment=assignment, student=student)
#         submission.submission_file = file_name
#         submission.save()
#         # return JsonResponse({'status': 'SUCCESS'})
#         return render(request, template_name='classroom/sending_a_task.html')
#
#     except Exception as e:
#         print(str(e))
#         submission = Submission(assignment=assignment, student=student, submission_file=file_name)
#         dt1 = datetime.now()
#         dt2 = datetime.combine(assignment.due_date, assignment.due_time)
#         time = timesince(dt1, dt2)
#         if time[0] == '0':
#             submission.submitted_on_time = False
#         submission.save()
#         # return JsonResponse({'status': 'SUCCESS'})
#     return render(request, template_name='classroom/sending_a_task.html')


def mark_submission(request, submission_id):
    submission = Submission.objects.get(pk=submission_id)
    if request.method == 'POST':
        marks = request.POST.get('submission_marks')
        status = request.POST.get('status')
        submission.marks_alloted = marks
        submission.status = status
        submission.save()
        return redirect('assignment_summary', submission.assignment.id)
    return render(request, template_name='classroom/mark_submission.html', context={'submission': submission})


def sending_a_task(request, pk):
    assignment = Assignment.objects.get(pk=pk)
    student = Student.objects.get(classroom=assignment.classroom, student=request.user.id)
    submission = Submission.objects.filter(assignment=assignment, student=student).first()
    file = request.POST.get('lol')
    if request.method == 'POST':
        # form = SubmitAssignmentForm(data=request.POST)
        if file:
            print('valid')
            submission = Submission(assignment=assignment, student=student, submission_file=file)
            submission.save()
            return redirect('render_class', assignment.classroom.id)
    # form = SubmitAssignmentForm()
    return render(request, template_name='classroom/sending_a_task.html', context={'submission': submission, 'assignment': assignment})


def group_list(request, pk):
    classroom = Classroom.objects.get(id=pk)
    students = Student.objects.filter(classroom=classroom)
    teacher = Teacher.objects.get(classroom=classroom)
    user = MyUser.objects.filter(is_active=True)
    # mentor = Student.objects.filter(student=user.statu)
    return render(request, template_name='classroom/group_list.html', context={'classroom': classroom, 'students': students, 'teacher': teacher})


def add_student(request, pk):
    classroom = Classroom.objects.get(id=pk)
    form = StudentAddForm()
    if request.method == 'POST':
        print(form)
        if form.is_valid():
            student = Student.objects.create(student=form, classroom=classroom)
            return redirect('render_class', classroom.id)
        form = StudentAddForm()
    return render(request, template_name='classroom/add_student.html', context={'classroom': classroom, 'form': form})

