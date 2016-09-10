from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


class ProfileDetailTest(TestCase):

    def setUp(self):
        self.joker = get_user_model().objects.create_user(email='joker@dc.com',
                                                          first_name='Mister',
                                                          last_name='J')

    def test_detail_view_with_existing_profile(self):
        self.client.force_login(self.joker)
        url = reverse('profiles:profile', args=(self.joker.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        harley = get_user_model().objects.create_user(email='harley@dc.com',
                                                          first_name='Harley',
                                                          last_name='Quinn')
        url = reverse('profiles:profile', args=(harley.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


    def test_detail_view_with_non_existing_profile(self):
        self.client.force_login(self.joker)
        url = reverse('profiles:profile', args=(101,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_detail_view_anonymous_user(self):
        url = reverse('profiles:profile', args=(self.joker.id,))
        response = self.client.get(url)
        expected_url = '/login/?next=/profile/{}/'.format(self.joker.id)
        self.assertRedirects(response, expected_url)


class GoToProfileTest(TestCase):

    def test_profile_view_logged_in_user(self):
        self.joker = get_user_model().objects.create_user(email='joker@dc.com',
                                                          first_name='Mister',
                                                          last_name='J')
        self.client.force_login(self.joker)
        url = reverse('profiles:go-to-profile')
        response = self.client.get(url)
        expected_url = reverse('profiles:profile', args=(self.joker.id,))
        self.assertRedirects(response, expected_url)

    def test_profile_view_anonymous_user(self):
        url = reverse('profiles:go-to-profile')
        response = self.client.get(url)
        expected_url = '/login/?next=/profile/'
        self.assertRedirects(response, expected_url)
