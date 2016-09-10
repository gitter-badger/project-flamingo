from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


from profiles.views import ProfileView
from profiles.models import Profile


class ProfileDetailTest(TestCase):

    def setUp(self):
        self.joker = get_user_model().objects.create_user(email='joker@dc.com',
                                                          first_name='Mister',
                                                          last_name='J')
        self.joker_profile = Profile.objects.get(user=self.joker)

    def test_detail_view_with_existing_profile(self):
        url = reverse('profile', args=(self.joker.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail_view_with_existing_profile(self):
        self.client.force_login(self.joker)
        response = self.client.get('/profile/')
        expected_url = '/profile/{}/'.format(self.joker.id)
        self.assertRedirects(response, expected_url)
