from django.core.validators import MaxValueValidator, MinValueValidator
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
        null=True,
    )
    bio = models.TextField(
        'Биография',
        blank=True,
        null=True,
    )
    role = models.CharField(
        max_length=40,
        choices=CHOICES,
        default='user'
    )
    # confirmation_code = models.CharField(
    #     max_length=250,
    #     blank=True,
    #     null=True,
    # )
    # password = models.CharField(
    #     max_length=250,
    #     blank=True,
    #     null=True,
    # )

    @property
    def is_authenticated(self):
        return self.role == 'user'

    @property
    def is_moderator(self):
        return self.role == 'moderator'
    
    @property
    def is_admin(self):
        return self.role == 'admin'
    
    # @property
    # def is_superuser(self):
    #     return self.role == 'admin'
    

    def __str__(self):
        return f'username: {self.username}, email: {self.email}'
    
    class Meta:
        ordering = ['id']


class Category(models.Model):
    name = models.CharField(
        'Название категории',
        max_length=200,
        null=True,
    )
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
        null=True,
    )
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
        null=True,
    )
    year = models.IntegerField(
        'Год выпуска',
        validators=(year_validator,),
        null=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
        null=True,
        blank=True,
    )
    description = models.TextField(
        'Описание',
        null=True,
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='genre',
        verbose_name='жанр',
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Рейтинг',
        validators=[
            MinValueValidator(1, 'Допустимы значения от 1 до 10'),
            MaxValueValidator(10, 'Допустимы значения от 1 до 10')
        ]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['pub_date']


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['pub_date']
