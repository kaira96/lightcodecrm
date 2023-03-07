from django.db import models
from django.conf import settings
from datetime import datetime


class Classroom(models.Model):
    classroom_name = models.CharField(max_length=99, verbose_name='Название')
    section = models.CharField(max_length=99, verbose_name='Раздел')
    class_code = models.CharField(max_length=10, default='0000000')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.classroom_name


class Student(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Студент')
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return str(self.student)

    def save(self, *args, **kwargs):
        user = self.student
        user.status = 2
        user.save()
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студент'


class Teacher(models.Model):
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Ментор')
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return str(self.teacher)

    def save(self, *args, **kwargs):
        user = self.teacher
        user.status = 4
        user.save()
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Ментор'
        verbose_name_plural = 'Менторы'


class Assignment(models.Model):
    assignment_name = models.CharField(max_length=50, verbose_name='Название')
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    due_date = models.DateField(verbose_name='Срок сдачи')
    due_time = models.TimeField(default=datetime.now().time(), verbose_name='Время сдачи')
    posted_date = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    instruction = models.TextField(verbose_name='Инструкция')
    total_marks = models.PositiveSmallIntegerField(default=100, verbose_name='Максимальное количество баллов')

    def __str__(self):
        return self.assignment_name

    class Meta:
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'


class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, verbose_name='Задание')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='Студент')
    submitted_date = models.DateField(auto_now_add=True, verbose_name='Дата отправки')
    submitted_time = models.TimeField(auto_now_add=True, verbose_name='Время отправки')
    submitted_on_time = models.BooleanField(default=True, verbose_name='Отправлено вовремя?')
    marks_alloted = models.PositiveSmallIntegerField(default=0, verbose_name='Оценка')
    submission_file = models.FileField(upload_to='documents', verbose_name='Файл')
    status = models.PositiveSmallIntegerField(
        choices=(
            (1, 'Отправлено'),
            (2, 'Переделать'),
            (3, 'Выполнено'),
        ),
        default=1
    )

    def __str__(self):
        return str(self.student)

    class Meta:
        verbose_name = 'Задания студентов'
        verbose_name_plural = 'Задания студентов'

