from django.db import models
from django.contrib.auth.models import AbstractUser


# class Roles(models.TextChoices):
#     USER = 'user',
#     MODERATIOR = 'moderator',
#     ADMIN = 'admin'

CHOICES = (
    ('User', 'зарегистрированный пользователь'),
    ('Moderator', 'модератор'),
    ('Admin', 'администратор'),
)


class User(AbstractUser):
    bio = models.TextField(
        'Биография',
        null=True,
        blank=True,
    ),
    email = models.EmailField(
        null=False,
        blank=False,
    ),
    role = models.CharField(
        max_length=16,
        choices=CHOICES,
        #choices=Roles.choices,
        #default=Roles.USER,
    )


class Title(models.Model):
    pass


class Category(models.Model):
    pass


class Genre(models.Model):
    pass
