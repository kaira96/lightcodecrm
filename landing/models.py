from django.db import models
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField
from googletrans import Translator
from bs4 import BeautifulSoup


User = get_user_model()

translator = Translator(service_urls=[
            'translate.google.com',
            'translate.google.co.kr',
        ])


class StudyingTime(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название')

    def save(self, *args, **kwargs):

        text_title = self.title

        ky_title = translator.translate(str(text_title), 'ky')
        # print(a.text)
        self.title_ky = ky_title.text

        super().save()

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

    def save(self, *args, **kwargs):

        text_title = self.title
        text_description = self.description
        text_additional_info = self.additional_info

        ky_title = translator.translate(str(text_title), 'ky')
        # print(a.text)
        self.title_ky = ky_title.text

        ky_description = translator.translate(str(text_description), 'ky')
        # print(a.text)
        self.description_ky = ky_description.text

        ky_additional_info = translator.translate(str(text_additional_info), 'ky')
        # print(a.text)
        self.additional_info_ky = ky_additional_info.text

        super().save()

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

    def save(self, *args, **kwargs):

        text_name = self.name
        text_direction = self.direction
        text_description = self.description

        ky_name = translator.translate(str(text_name), 'ky')
        # print(a.text)
        self.name_ky = ky_name.text

        ky_direction = translator.translate(str(text_direction), 'ky')
        # print(a.text)
        self.direction_ky = ky_direction.text

        ky_description = translator.translate(str(text_description), 'ky')
        # print(a.text)
        self.description_ky = ky_description.text

        super().save()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Section(models.Model):
    title = models.CharField(max_length=123, verbose_name='Название')
    slug = models.SlugField()
    id_section = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')
    description = models.TextField(verbose_name='Описание для подраздела', blank=True, null=True)

    def save(self, *args, **kwargs):

        text_title = self.title
        text_description = self.description

        ky_title = translator.translate(str(text_title), 'ky')
        # print(a.text)
        self.title_ky = ky_title.text

        ky_description = translator.translate(str(text_description), 'ky')
        # print(a.text)
        self.description_ky = ky_description.text

        super().save()

    def __str__(self):
        full_path = [self.title]
        k = self.id_section
        while k is not None:
            full_path.append(k.title)
            k = k.id_section
        return ' -> '.join(full_path[::-1])

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'


class Article(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Ментор')
    topic_name = models.CharField(max_length=80, verbose_name='Название темы')
    slug = models.SlugField()
    body = RichTextField(verbose_name='Контент')
    section = models.ForeignKey(Section, on_delete=models.CASCADE, verbose_name='Раздел')
    created_date = models.DateField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return str(self.section)

    def save(self, *args, **kwargs):

        text_topic_name = self.topic_name

        ky_topic_name = translator.translate(str(text_topic_name), 'ky')
        self.topic_name_ky = ky_topic_name.text

        soup = BeautifulSoup(self.body, 'html.parser')
        text_body = [i.replace('.', '. ') for i in list(soup.stripped_strings)]
        dct = {i: translator.translate(i, 'ky').text for i in text_body}

        for k, v in dct.items():
            self.body_ky = self.body_ky.replace(k, v)

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
        if user.status == 2 or user.status == 1:
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




