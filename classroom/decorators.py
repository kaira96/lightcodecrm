from django.shortcuts import redirect

from .models import Classroom, Student, Teacher, Assignment


def access_class(redirect_to):
    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            is_a_teacher, is_a_student = False, False
            try:
                classroom = Classroom.objects.get(id=kwargs['id'])
            except Exception as e:
                return redirect('home')

            teacher_count = Teacher.objects.filter(teacher=request.user.id, classroom=classroom).count()
            if teacher_count > 0:
                is_a_teacher = True

            student_count = Student.objects.filter(student=request.user.id, classroom=classroom).count()
            if student_count > 0:
                is_a_student = True

            if not (is_a_student or is_a_teacher):
                return redirect('home')

            return view_method(request, *args, **kwargs)

        return _arguments_wrapper

    return _method_wrapper


def login_excluded(redirect_to):
    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_to)
            return view_method(request, *args, **kwargs)

        return _arguments_wrapper

    return _method_wrapper


def teacher_required(redirect_to):
    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            if kwargs.get('classroom'):
                query_id = kwargs['classroom']
            elif kwargs.get('assignment'):
                try:
                    assignment = Assignment.objects.get(pk=kwargs['assignment'])
                except Exception as e:
                    print(str(e))
                    return redirect('home')
                query_id = assignment.classroom.id

            try:
                classroom = Classroom.objects.get(pk=query_id)
            except Exception as e:
                print(str(e))
                return redirect('render_class', id=query_id)

            teacher_count = Teacher.objects.filter(teacher=request.user, classroom=classroom).count()
            if teacher_count == 0:
                return redirect('render_class', id=query_id)
            return view_method(request, *args, **kwargs)

        return _arguments_wrapper

    return _method_wrapper


def student_required(redirect_to):
    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            print(kwargs)
            if kwargs.get('classroom'):
                query_id = kwargs['classroom']
            elif kwargs.get('assignment'):
                try:
                    assignment = Assignment.objects.get(pk=int(kwargs['assignment']))
                except Exception as e:
                    return redirect(to='home')
                query_id = assignment.classroom.id

            try:
                classroom = Classroom.objects.get(pk=query_id)
            except Exception as e:
                return redirect(to='render_class', id=query_id)

            student_count = Student.objects.filter(student=request.user, classroom=classroom).count()
            if student_count == 0:
                return redirect(to='render_class', id=query_id)
            return view_method(request, *args, **kwargs)

        return _arguments_wrapper

    return _method_wrapper

