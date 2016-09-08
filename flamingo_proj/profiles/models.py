from __future__ import unicode_literals
from datetime import datetime


from django.db import models
from django.contrib.auth import password_validation
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


from .utils import generate_random_username


class MyUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, first_name, last_name,
                     **extra_fields):
        if not email:
            raise ValueError('The email must be set.')
        email = self.normalize_email(email)
        user = MyUser(email=email, first_name=first_name, last_name=last_name,
                      **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, first_name, last_name, password=None,
                    **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, first_name, last_name, **extra_fields)

    def create_superuser(self, email, password, first_name, last_name,
                         **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, first_name, last_name, **extra_fields)


class MyUser(AbstractUser):
    email = models.EmailField(
        'email address',
        unique=True,
        error_messages={
            'unique': "A user with that email address already exists.",
        }
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = MyUserManager()

    def save(self, *args, **kwargs):
        self.username = generate_random_username()
        self.full_clean()
        super(MyUser, self).save(*args, **kwargs)
        if self._password is not None:
            password_validation.password_changed(self._password, self)
            self._password = None


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True)
    birthdate = models.DateField(blank=True, null=True)
    follows = models.ManyToManyField('Profile', related_name='followed_by',
                                     symmetrical=False, blank=True)
    rating = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )


    def clean_fields(self, exclude=None):
        if self.rating < 0 or self.rating > 5.0:
            raise ValidationError('Invalid rating value')
        if self in self.follows.all():
            raise ValidationError('User cannot follow self')
        super(Profile, self).clean_fields()

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.get_full_name()

    @property
    def age(self):
        today = datetime.date.today()
        age = (today.year - self.birthdate.year) - \
            int((today.month, today.day) <
                (self.birthdate.month, self.birthdate.day))
        return age
