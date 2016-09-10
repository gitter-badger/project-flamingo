import datetime


from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import ValidationError


from profiles.models import Profile


MyUser = get_user_model()


class MyUserTestCase(TestCase):
    email = 'test_user@test.test'
    first_name = 'Harley'
    last_name = 'Quinn'

    def setUp(self):
        self.test_user = MyUser.objects.create_user(
            email=self.email, first_name=self.first_name, last_name=self.last_name)

    def test_user_creation(self):
        now = timezone.now()

        self.assertEqual(MyUser.objects.all().count(), 1)
        self.assertEqual(MyUser.objects.all()[0], self.test_user)

        self.assertEqual(self.test_user.email, self.email)
        self.assertEqual(self.test_user.first_name, self.first_name)
        self.assertEqual(self.test_user.last_name, self.last_name)
        self.assertEqual(self.test_user.date_joined.date(), now.date())

        self.assertTrue(self.test_user.is_active)
        self.assertFalse(self.test_user.is_staff)
        self.assertFalse(self.test_user.is_superuser)

    def test_user_get_name(self):
        self.assertEqual(self.test_user.get_short_name(), self.first_name)
        self.assertEqual(
            self.test_user.get_full_name(),
            self.first_name + ' ' + self.last_name)


class MyUserManager(TestCase):
    email = 'test_user@test.test'
    password = 'test1234'
    first_name = 'Harley'
    last_name = 'Quinn'

    def test_create_user(self):
        test_user = MyUser.objects.create_user(
            email=self.email, first_name=self.first_name, last_name=self.last_name)
        self.assertEqual(MyUser.objects.all()[0], test_user)

        self.assertTrue(test_user.is_active)
        self.assertFalse(test_user.is_staff)
        self.assertFalse(test_user.is_superuser)

        with self.assertRaises(ValueError):
            MyUser.objects.create_user(email='', first_name=self.first_name,
                                       last_name=self.last_name)

        with self.assertRaises(ValueError):
            MyUser.objects.create_user(email=None, first_name=self.first_name,
                                       last_name=self.last_name)

    def test_create_superuser(self):
        self.email = 'superuser@test.test'
        test_user = MyUser.objects.create_superuser(
            email=self.email, password=self.password,
            first_name=self.first_name, last_name=self.last_name
        )
        self.assertEqual(MyUser.objects.all()[0], test_user)

        self.assertTrue(test_user.is_active)
        self.assertTrue(test_user.is_staff)
        self.assertTrue(test_user.is_superuser)

        with self.assertRaises(ValueError):
            MyUser.objects.create_user(email='', password=self.password,
                        first_name=self.first_name, last_name=self.last_name)


class ProfileTestCase(TestCase):

    def setUp(self):
        self.test_user = MyUser.objects.create_user(
            email='test@test.test', first_name='Harley', last_name='Quinn')

    def test_create_user_profile(self):
        self.assertEqual(Profile.objects.all().count(), 1)
        test_profile = Profile.objects.all()[0]
        self.assertEqual(test_profile.user, self.test_user)

    def test_profile_rating(self):
        test_profile = Profile.objects.all()[0]
        test_profile.rating = -2
        with self.assertRaises(ValidationError):
            test_profile.save()

        test_profile.rating = 6
        with self.assertRaises(ValidationError):
            test_profile.save()

        test_profile.rating = 4.5
        self.assertEqual(test_profile.rating, 4.5)

    def test_profile_follows(self):
        test_profile = Profile.objects.all()[0]
        friend = MyUser.objects.create_user(email="test@local.test",
                                            first_name="test", last_name="person")
        friend_profile = Profile.objects.get(user=friend)
        test_profile.follows.add(friend_profile)
        self.assertIn(friend_profile, test_profile.follows.all())
        test_profile.follows.add(test_profile)
        with self.assertRaises(ValidationError):
            test_profile.save()

    def test_profile_age(self):
        test_profile = Profile.objects.all()[0]
        test_profile.birthdate = datetime.date(day=8, month=7, year=1995)
        self.assertEqual(test_profile.age, 21)
