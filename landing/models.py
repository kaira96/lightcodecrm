from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField
from django.template.defaultfilters import slugify


User = get_user_model()


class StudyingTime(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Время обучения'
        verbose_name_plural = 'Время обучения'


class CourseForLanding(models.Model):
    title = models.CharField(max_length=123, verbose_name=('Название'))
    slug = models.SlugField()
    cover = models.ImageField(upload_to='media/image/', verbose_name=('Обложка'))
    description = models.TextField(verbose_name=('Описание о языке'))
    studying_time = models.ManyToManyField(StudyingTime, verbose_name='Время обучения')
    format = models.ManyToManyField('srm.LearningFormat', verbose_name='Формат обучения')
    additional_info = models.TextField(verbose_name='Информация о курсе', blank=True, null=True)
    teacher = models.ForeignKey('srm.Employee', on_delete=models.PROTECT, verbose_name='Ментор')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=('Дата создания'))
    is_active = models.BooleanField(default=True, verbose_name=('Активен'))

    def studying_time_names(self):
        return " %s" % (", ".join([formats.title for formats in self.studying_time.all()]))

    def format_names(self):
        return " %s" % (", ".join([formats.title for formats in self.format.all()]))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Курс для Лэндинга'
        verbose_name_plural = 'Курс для Лэндинга'


class Review(models.Model):
    name = models.CharField(max_length=70, verbose_name='Имя')
    direction = models.CharField(max_length=50, verbose_name='Направление')
    description = models.TextField(verbose_name=('Описание'), max_length=515)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=('Дата создания'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Section(models.Model):
    title = models.CharField(max_length=123, verbose_name='Название')
    slug = models.SlugField()
    id_section = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')

    def __str__(self):
        full_path = [self.title]
        k = self.id_section
        while k is not None:
            full_path.append(k.title)
            k = k.id_section
        return ' -> '.join(full_path[::-1])

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.title)
    #     super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'


class Article(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Ментор')
    topic_name = models.CharField(max_length=50, verbose_name='Название темы')
    slug = models.SlugField()
    body = RichTextField(verbose_name='Контент')
    section = models.ForeignKey(Section, on_delete=models.CASCADE, verbose_name='Раздел')
    created_date = models.DateField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return str(self.section)

    def save(self, *args, **kwargs):
        user = self.teacher
        user.status = 4
        user.save()
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class SubscriptionToCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    course = models.ForeignKey(Section, on_delete=models.CASCADE, verbose_name='Курс')
    created_date = models.DateField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        user = self.user
        user.status = 2
        user.save()
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Подписка на курс'
        verbose_name_plural = 'Подписка на курс'
        unique_together = ['user', 'course']


class Stream(models.Model):
    url = models.TextField(verbose_name='Ссылка на прямой эфир')
    start_time = models.DateTimeField(verbose_name='Время начала стрима')
    end_time = models.DateTimeField(verbose_name='Время окончания стрима')
    is_active = models.BooleanField(verbose_name='Актуально?')
    # def save(self, *args, **kwargs):
    #     # Получить все объекты Stream кроме текущего
    #     other_streams = Stream.objects.exclude(pk=self.pk)
    #     # Удалить все полученные объекты
    #     other_streams.delete()
    #     super(Stream, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Прямой эфир'
        verbose_name_plural = 'Прямой эфир'




