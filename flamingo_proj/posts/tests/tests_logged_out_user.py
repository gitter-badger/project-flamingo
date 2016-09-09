from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from django.urls import reverse
MyUser = get_user_model()


class TestLoggedOutUser(TestCase):
    client = Client()

    def setUp(self):
        self.u = MyUser.objects.create_user(username='dasde',
                                            email='test@gmail.com',
                                            first_name="Simo", last_name='Rolev')
        self.u.set_password('testpass')
        self.u.save()

    def test_home_is_responding(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_feed_redirects_to_login_if_you_are_not_logged(self):
        response = self.client.get(reverse('feed'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/?next=/feed/')

    def test_signup_is_responding(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_profiles_redirect_on_try_to_access(self):
        response = self.client.get(reverse('profile', args=[1]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/?next=/profile/1/')
