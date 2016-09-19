import datetime


from django.test import TestCase
from django.contrib.auth import get_user_model


from profiles.forms import ProfileForm
from profiles.models import Profile


class ProfileFormTestCase(TestCase):

    def setUp(self):
        self.harley = get_user_model().objects.create_user(email='harley@dc.com',
                                                           first_name='Harley',
                                                           last_name='Quinn')
        self.harley_profile = Profile.objects.get(user=self.harley)

    def test_profile_birthdate_validation(self):
        form_data = {'user': self.harley.id, 'birthdate': 'date', 'rating': '5'}
        form = ProfileForm(instance=self.harley_profile, data=form_data)
        self.assertFalse(form.is_valid())
        form_data['birthdate'] = '1980-10-10'
        form = ProfileForm(instance=self.harley_profile, data=form_data)
        self.assertTrue(form.is_valid())

    def test_profile_follows_validation(self):
        form_data = {'user': self.harley.id, 'follows': [self.harley_profile], 'rating': '5'}
        form = ProfileForm(instance=self.harley_profile, data=form_data)
        self.assertFalse(form.is_valid())
        joker = get_user_model().objects.create_user(email='joker@dc.com',
                                                     first_name='Joker',
                                                     last_name='X')
        joker_profile = Profile.objects.get(user=joker)
        form_data['follows'] = [joker_profile]
        form = ProfileForm(instance=self.harley_profile, data=form_data)
        self.assertTrue(form.is_valid())
        form_data['follows'] = [joker_profile, self.harley_profile]
        form = ProfileForm(instance=self.harley_profile, data=form_data)
        self.assertFalse(form.is_valid())
