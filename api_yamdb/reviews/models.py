from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser

# from django.contrib.auth.tokens import default_token_generator
# from django.db.models.signals import post_save
# from django.dispatch import receiver

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
    )
    bio = models.TextField(
        'Биография',
        blank=True,
        null=True,
    )
    role = models.CharField(
        max_length=50,
        choices=CHOICES,
        default='user'
    )
    confirmation_code = models.CharField(
        max_length=250,
        blank=True,
        null=True,
    )
    password = models.CharField(
        max_length=254,
        blank=True,
        null=True,
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

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
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['id']

    def __str__(self):
        return f'username: {self.username}, email: {self.email}'


# @receiver(post_save, sender=User)
# def post_save(sender, instance, created, **kwargs):
#     if created:
#         confirmation_code = default_token_generator.make_token(
#             instance
#         )
#         instance.confirmation_code = confirmation_code
#         instance.save()


class Category(models.Model):
    name = models.CharField(
        'Название категории',
        max_length=256,
    )
    slug = models.SlugField(
        'Адрес категории',
        unique=True,
        db_index=True,
        max_length=50,
    )

    
    class Meta:
        verbose_name = 'Катеория'
        verbose_name_plural = 'Категории' 

    def __str__(self):
        return f'{self.name} {self.slug}'


class Genre(models.Model):
    name = models.CharField(
        'Название жанра',
        max_length=256,
    )
    slug = models.SlugField(
        'Адрес жанра',
        unique=True,
        db_index=True,
        max_length=50,
    )


    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return f'{self.name} {self.slug}'


class Title(models.Model):
    name = models.CharField(
        'Название произведения',
        max_length=256,
    )
    year = models.IntegerField(
        'Год выпуска',
        validators=(year_validator,),
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
        max_length=256,
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='genre',
        verbose_name='жанр',
    )


    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

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
    
    def __str__(self):
        return self.text


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
    
    def __str__(self):
        return self.text
