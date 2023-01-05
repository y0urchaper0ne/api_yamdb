from django.db import models
from django.contrib.auth.models import AbstractUser


# class Roles(models.TextChoices):
#     USER = 'user',
#     MODERATIOR = 'moderator',
#     ADMIN = 'admin'

CHOICES = (
    ('user', 'зарегистрированный пользователь'),
    ('moderator', 'модератор'),
    ('admin', 'администратор'),
)


class User(AbstractUser):
    bio = models.TextField(
        'Биография',
        blank=True,
        null=True,
    ),
    email = models.EmailField(
        max_length=254,
        unique=True,
    ),
    role = models.CharField(
        max_length=16,
        choices=CHOICES,
        default='user'
    )

    def __str__(self):
        return f'username: {self.username}, email: {self.email}'


class Category(models.Model):
    name = models.CharField(
        'Название категории',
        max_length=200,
    ),
    slug = models.SlugField(
        'Адрес категории',
        unique=True,
        db_index=True,
        default=name

    )
    
    def __str__(self):
        return f'{self.name} {self.slug}'


class Genre(models.Model):
    name = models.CharField(
        'Название жанра',
        max_length=200,
    ),
    slug = models.SlugField(
        'Адрес жанра',
        unique=True,
        db_index=True,
        default=name
    )
    
    def __str__(self):
        return f'{self.name} {self.slug}'


class Title(models.Model):
    name = models.CharField(
        'Название произведения',
        max_length=200,
    ),
    year = models.IntegerField(
        'Год выпуска',
    ),
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
        null=True,
        blank=True,
    ),
    description = models.TextField(
        'Описание',
        null=True,
        blank=True,
    ),
    genre = models.ManyToManyField(
        Genre,
        related_name='genre',
        verbose_name='жанр',
    )

    def __str__(self):
        return self.name
