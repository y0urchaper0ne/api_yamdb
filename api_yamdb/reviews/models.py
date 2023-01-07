from django.db import models
from django.contrib.auth.models import AbstractUser

from .validators import year_validator

# USER = 'user',
# MODERATOR = 'moderator',
# ADMIN = 'admin'

CHOICES = (
    ('user', 'зарегистрированный пользователь'),
    ('moderator', 'модератор'),
    ('admin', 'администратор'),
)


class User(AbstractUser):
    email = models.EmailField(
        max_length=254,
        unique=True,
    ),
    first_name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    ),
    last_name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    ),
    bio = models.TextField(
        'Биография',
        blank=True,
        null=True,
    ),
    role = models.CharField(
        max_length=40,
        choices=CHOICES,
        default='user'
    ),
    confirmation_code = models.CharField(
        max_length=250,
        blank=True,
        null=True,
    ),
    password = models.CharField(
        max_length=250,
        blank=True,
        null=True,
    ),

    @property
    def is_authenticated(self):
        return self.role == 'user'

    @property
    def is_moderator(self):
        return self.role == 'moderator'
    
    @property
    def is_admin(self):
        return self.role == 'admin'
    
    @property
    def is_superuser(self):
        return self.role == 'admin'
    

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
        validators=(year_validator,)
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
