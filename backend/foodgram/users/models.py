from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
                                        UserManager)
from django.core.validators import RegexValidator
from django.db import models


class CustomUserManager(UserManager):

    def create_user(
        self, email, username,
        first_name, last_name, password, **other_fields
    ):

        if not email:
            raise ValueError('Email должен быть указан')
        if not username:
            raise ValueError('Username должен быть указан')
        if not first_name:
            raise ValueError('Имя должно быть указано')
        if not last_name:
            raise ValueError('Фамилия должна быть указана')
        if not password:
            raise ValueError('Пароль должен быть указан')

        email = self.normalize_email(email)
        user = self.model(
            email=email, username=username,
            first_name=first_name, last_name=last_name, **other_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(
        self, email, username, first_name, last_name, password, **other_fields
    ):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(
            email, username, first_name, last_name,
            password, **other_fields
        )


class CustomUser(AbstractBaseUser, PermissionsMixin):
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    email = models.EmailField(blank=False, null=False, unique=True)
    username = models.CharField(
        max_length=150,
        blank=False,
        null=False,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message=(
                    """Введите корректный username. """
                    """Допускаются любые буквы, цифры, """
                    """а также символы "_", "@", ".", "-", "+"."""
                )
            )
        ]
    )
    first_name = models.CharField(max_length=150, blank=False, null=False)
    last_name = models.CharField(max_length=150, blank=False, null=False)
    password = models.CharField(max_length=150, blank=False, null=False)
    link = "Edit"

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.username
