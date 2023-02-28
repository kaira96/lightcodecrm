from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField


class MyUserManager(BaseUserManager):
    def create_user(self, phone_number, username, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """

        user = self.model(
            phone_number=phone_number,
            username=username
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, username, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            phone_number=phone_number,
            username=username,
            password=password,

        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    # email = models.EmailField(
    #     verbose_name=('Адрес электронной почты'),
    #     max_length=255,
    #     unique=True,
    # )
    username = models.CharField(
        max_length=50,
        verbose_name='Имя пользователя',
        unique=True,
    )
    phone_number = PhoneNumberField(
        region='KG',
        verbose_name=('Номер телефона'),
        unique=True
    )
    status = models.PositiveSmallIntegerField(
        choices=(
            (1, 'Простой пользователь'),
            (2, 'Студент'),
            (3, 'Менеждер'),
            (4, 'Ментор'),
            (5, 'Копирайтер'),
        ),
        default=1,
        verbose_name=('Статус')
    )
    created_date = models.DateField(auto_now_add=True, verbose_name='Дата создания аккаунта')
    is_active = models.BooleanField(
        default=True,
        verbose_name=('Пользователь активен?')
    )
    is_admin = models.BooleanField(
        default=False,
        verbose_name=('Админ')
    )

    objects = MyUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username', ]

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

