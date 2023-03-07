from decimal import Decimal

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.html import format_html
from django.core.exceptions import ValidationError
from datetime import datetime


class Role(models.Model):
    title = models.CharField(max_length=70, verbose_name='Название')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'


class StudyingTime(models.Model):
    title = models.CharField(max_length=15, verbose_name='Название')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Время обучения'
        verbose_name_plural = 'Время обучения'


class LearningFormat(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Формат обучения'
        verbose_name_plural = 'Форматы обучения'


class Course(models.Model):
    title = models.CharField(max_length=123, verbose_name=('Название'))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=('Дата создания'))
    is_active = models.BooleanField(default=True, verbose_name=('Активен'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Employee(models.Model):
    full_name = models.CharField(max_length=123, verbose_name='ФИО')
    image = models.ImageField(upload_to='media/image', verbose_name='Фотография')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, verbose_name='Роль')
    salary = models.DecimalField(decimal_places=2, max_digits=12, default=0.00, verbose_name='Зарплата')
    description = models.TextField(verbose_name=('Описание для Лэндинга'), blank=True, null=True)
    course = models.ManyToManyField(Course, verbose_name='Курс', blank=True, null=True)
    studying_time = models.ManyToManyField(StudyingTime, verbose_name='Время обучения', blank=True, null=True)
    format = models.ManyToManyField(LearningFormat, verbose_name='Формат обучения', blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_active = models.BooleanField(default=True, verbose_name='Активен')

    def course_names(self):
        return " %s" % (", ".join([formats.title for formats in self.course.all()]))

    def format_names(self):
        return " %s" % (", ".join([formats.title for formats in self.format.all()]))

    def studying_time_names(self):
        return " %s" % (", ".join([formats.title for formats in self.studying_time.all()]))

    def __str__(self):
        return f'{self.full_name} | {self.course_names()} | {self.studying_time_names()} | {self.format_names()}'

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'


class Currency(models.Model):
    title = models.CharField(max_length=40, verbose_name='Название')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюты'


class PaymentMethod(models.Model):
    title = models.CharField(max_length=70, verbose_name='Название')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Способ оплаты'
        verbose_name_plural = 'Способы оплаты'


class Student(models.Model):
    full_name = models.CharField(max_length=80, verbose_name=('ФИО'))
    phone_number = models.CharField(verbose_name=('Номер телефона'), max_length=15)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name='Курс',
        related_name='student')
    teacher = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='Ментор', blank=True, null=True)
    studying_time = models.PositiveSmallIntegerField(
        choices=(
            (1, 'Утро'),
            (2, 'День'),
            (3, 'Вечер'),
            (4, 'Ночь'),
        ),
        verbose_name='Время обучения',
        blank=True,
        null=True
    )
    format = models.ForeignKey(LearningFormat, on_delete=models.CASCADE, verbose_name='Формат обучения', blank=True, null=True)
    certificate = models.PositiveSmallIntegerField(default=0, verbose_name='Сертификат')
    url = models.URLField(blank=True, null=True)
    total_payment = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        default=0.00,
        verbose_name='Общая оплата',
        blank=True,
        null=True)
    last_payment_date = models.DateField(verbose_name='Дата последней оплаты', blank=True, null=True)
    remainder = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        default=0.00,
        verbose_name='Остаток')
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    is_graduate = models.BooleanField(default=False, verbose_name='Выпускник')
    created_date = models.DateField(auto_now_add=True, verbose_name='Дата создания')

    # def save(self, *args, **kwargs):
    #     if self.remainder == 0:
    #         remainder = Decimal(str(self.remainder))
    #         remainder -= Decimal(str(self.total_payment))
    #     return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.full_name}  | {self.teacher} | {self.studying_time} | {self.format}'

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'


class Expense(models.Model):
    title = models.CharField(max_length=123, verbose_name='Название')
    value = models.DecimalField(decimal_places=2, max_digits=12, default=0.00, verbose_name='Цена')
    flow_type = models.PositiveSmallIntegerField(
        choices=(
            (1, 'Постоянный'),
            (2, 'Одноразовый'),
            (3, 'Сотрудник'),
            (4, 'Возврат'),
        ),
        verbose_name='Тип расхода'
    )
    created_date = models.DateField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Расходы'
        verbose_name_plural = 'Расходы'


class Income(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='Студент')
    value = models.DecimalField(decimal_places=2, max_digits=12, default=0.00, verbose_name='Цена')
    payment_method = models.ForeignKey(
                PaymentMethod,
                on_delete=models.CASCADE,
                verbose_name='Способ оплаты',
                related_name='incomes',
            )
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, verbose_name='Валюта', blank=True, null=True)
    date_of_payment = models.DateField(verbose_name='Дата оплаты')
    created_date = models.DateField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return str(self.student)

    def save(self, *args, **kwargs):
        student = self.student
        student.total_payment += self.value
        student.last_payment_date = datetime.now().date()
        student.remainder -= self.value
        student.save()
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Доходы'
        verbose_name_plural = 'Доходы'


class Lead(models.Model):
    full_name = models.CharField(max_length=80, verbose_name=('ФИО'))
    phone_number = models.CharField(max_length=15, verbose_name=('Номер телефона'))
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name=('Курс'), blank=True, null=True)
    description = models.TextField(verbose_name=('Описание'), blank=True, null=True)
    is_add = models.BooleanField(default=False, verbose_name=('Добавить'))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=('Дата создания'))

    def __str__(self):
        return self.full_name

    # def clean(self):
    #     if self.is_add == True:
    #         if not self.course:
    #             raise ValidationError({'course': 'На какой курс хочет записаться Лид'})
    #     return super(Lead, self).clean()
    #
    # def save(self, *args, **kwargs):
    #     if self.is_add == True:
    #         Student.objects.create(
    #             full_name=self.full_name,
    #             phone_number=self.phone_number,
    #             course=self.course,
    #         )
    #     return super().save(*args, *kwargs)
    def create_student(self):
        if self.is_add == True:
            student = Student.objects.create(
                full_name=self.full_name,
                phone_number=self.phone_number,
                course=self.course,
                description=self.description
            )
            return student
        return None

    def clean(self):
        if self.is_add == True:
            if not self.course:
                raise ValidationError({'course': 'На какой курс хочет записаться Лид'})
        return super(Lead, self).clean()

    def save(self, *args, **kwargs):
        self.create_student()
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Лид'
        verbose_name_plural = 'Лиды'




