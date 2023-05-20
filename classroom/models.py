from django.db import models
from django.conf import settings
from datetime import datetime
from googletrans import Translator


translator = Translator(service_urls=[
            'translate.google.com',
            'translate.google.co.kr',
        ])


class Classroom(models.Model):
    classroom_name = models.CharField(max_length=99, verbose_name='Название')
    section = models.CharField(max_length=99, verbose_name='Раздел')
    class_code = models.CharField(max_length=10, default='0000000')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def save(self, *args, **kwargs):

        text_classroom_name = self.classroom_name
        text_section = self.section

        ky_classroom_name = translator.translate(str(text_classroom_name), 'ky')
        # print(a.text)
        self.classroom_name_ky = ky_classroom_name.text

        ky_section = translator.translate(str(text_section), 'ky')
        # print(a.text)
        self.section_ky = ky_section.text

        super().save()

    def __str__(self):
        return self.classroom_name


class Student(models.Model):
    student = models.ForeignKey('account.MyUser', on_delete=models.CASCADE, verbose_name='Студент')
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return str(self.student)

    def save(self, *args, **kwargs):
        user = self.student
        if user.status != 4:
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

    def save(self, *args, **kwargs):

        text_assignment_name = self.assignment_name
        text_instruction = self.instruction

        ky_assignment_name = translator.translate(str(text_assignment_name), 'ky')
        # print(a.text)
        self.assignment_name_ky = ky_assignment_name.text

        ky_instruction = translator.translate(str(text_instruction), 'ky')
        # print(a.text)
        self.instruction_ky = ky_instruction.text

        super().save()

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

