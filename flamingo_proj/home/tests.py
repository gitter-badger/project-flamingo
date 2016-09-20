from django.test import TestCase, Client
from posts.models import Post, Tag
from django.contrib.auth import get_user_model
from django.urls import reverse


MyUser = get_user_model()


class TestHome(TestCase):
    client = Client()

    def setUp(self):
        # Login a user
        self.u = MyUser.objects.create_user(username='dasde',
                                            email='test_logged@gmail.com',
                                            first_name="Simo", last_name='Rolev')
        self.u.set_password('testpass')
        self.u.save()
        self.login = self.client.login(email=self.u.email, password='testpass')

        self.p1 = Post(posted_by=self.u, content="Working out! #gym #flex")
        self.p1.save()
        self.p2 = Post(posted_by=self.u, content="Day two! #gym #secondday")
        self.p2.save()

        self.gym_tag = Tag.objects.get(tag="#gym")
        self.flex_tag = Tag.objects.get(tag="#flex")
        self.second_day_tag = Tag.objects.get(tag="#secondday")

        self.u2 = MyUser.objects.create_user(username='dasde',
                                            email='test_other@gmail.com',
                                            first_name="Iva", last_name='Petrova')

        self.u.profile.follows.add(self.u2.profile)
        self.p3 = Post(posted_by=self.u2, content="You follow me #right?")
        self.p3.save()

    def test_feed_response(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_connected_to_feed(self):
        response = self.client.get(reverse('home'))
        full_content = response.content
        feed_page_title = "<h1> You are at the feed page! </h1>"
        feed_page_you_are_logged_in = "<p> You are now logged in as Simo Rolev </p>"
        self.assertIn(feed_page_title, full_content)
        self.assertIn(feed_page_you_are_logged_in, full_content)

    def test_profile_contains_own_posts_and_no_other(self):
        response = self.client.get(reverse('profiles:profile', args=[1]))
        full_content = response.content
        own_post_one = 'Working out! <a href="/posts/tag/gym/">#gym</a> <a href="/posts/tag/flex/">#flex</a>'
        self.assertIn(own_post_one, full_content)
        own_post_two = "Day two!"
        self.assertIn(own_post_two, full_content)
        post_div_one = '<div class="post" id="post{}">'.format(self.p1.id)
        post_div_two = '<div class="post" id="post{}">'.format(self.p2.id)
        post_div_error = '<div class="post" id="post{}">'.format(self.p3.id)

        self.assertIn(post_div_one, full_content)
        self.assertIn(post_div_two, full_content)
        self.assertNotIn(post_div_error, full_content)

    def test_feed_posts_from_followed(self):
        response = self.client.get(reverse('home'))
        full_content = response.content
        followed_post_one = 'You follow me <a href="/posts/tag/right/">#right</a>?'
        self.assertIn(followed_post_one, full_content)

        post_div_one = '<div class="post" id="post{}">'.format(self.p3.id)
        post_div_error = '<div class="post" id="post{}">'.format(self.p1.id)

        self.assertIn(post_div_one, full_content)
        self.assertNotIn(post_div_error, full_content)
