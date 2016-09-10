from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from django.urls import reverse
MyUser = get_user_model()


class TestLoggedInUser(TestCase):
    client = Client()

    def setUp(self):
        self.u = MyUser.objects.create_user(username='dasde',
                                            email='test@gmail.com',
                                            first_name="Simo", last_name='Rolev')
        self.u.set_password('testpass')
        self.u.save()
        self.login = self.client.login(email=self.u.email, password='testpass')

    def test_valid_login(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse('profiles:profile', args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_invalid_login(self):
        login = self.client.login(email="fake@abv.bg", password='testpass')
        self.assertFalse(login)
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
