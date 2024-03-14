from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse

from custom_modules.services.utils import generate_unique_slugify


class User(AbstractUser):
    slug = models.SlugField(
        verbose_name='URL',
        max_length=255,
        blank=True,
        unique=True,
    )
    photo = models.ImageField(
        upload_to='photos/users/Y%/m%/d%',
        verbose_name='Фото',
        default='photos/default/default.jpg',
        blank=True,
        validators=[
            FileExtensionValidator(allowed_extensions=('png', 'jpg', 'jpeg')),
        ],
    )
    date_of_birth = models.DateField(
        verbose_name='Дата рождения',
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.username

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse('user', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slugify(self, self.username)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователь'
        db_table = 'users_users'
        ordering = ('username',)

