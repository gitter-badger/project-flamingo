from __future__ import unicode_literals


from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


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
        user.full_clean()
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


class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        'email address',
        unique=True,
        error_messages={
            'unique': "A user with that email address already exists.",
        }
    )

    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text='Designates whether the user can log into this admin site.',
    )

    is_active = models.BooleanField(
        'active',
        default=True,
        help_text='Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.',
    )

    date_joined = models.DateTimeField('date joined', auto_now_add=True)
    first_name = models.CharField(max_length=30, null=False, blank=False)
    last_name = models.CharField(max_length=30, null=False, blank=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = MyUserManager()

    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def get_short_name(self):
        return self.first_name


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True)
    birthdate = models.DateField(blank=True, null=True)
    follows = models.ManyToManyField('Profile', related_name='followed_by')
    rating = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )

    def __str__(self):
        return self.user.get_full_name()

    @property
    def age(self):
        today = datetime.date.today()
        age = (today.year - self.birthdate.year) - \
            int((today.month, today.day) <
                (self.birthdate.month, self.birthdate.day))
        return age
