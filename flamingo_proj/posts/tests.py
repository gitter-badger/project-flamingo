from django.test import TestCase, Client
from .models import Post, Tag
from django.contrib.auth import get_user_model

from django.urls import reverse
MyUser = get_user_model()


class TestPosts(TestCase):

    def setUp(self):
        self.u = MyUser(5, email='test@gmail.com', password='testpass', first_name="Simo")
        self.u.save()
        self.u2 = MyUser(6, email='test2@gmail.com', password='testpass', first_name="Simo2")
        self.u2.save()
        self.p1 = Post(posted_by=self.u, content="Working out! #gym #flex")
        self.p1.save()
        self.p2 = Post(posted_by=self.u, content="Day two! #gym #secondday")
        self.p2.save()

        self.gym_tag = Tag.objects.get(tag="#gym")
        self.flex_tag = Tag.objects.get(tag="#flex")
        self.second_day_tag = Tag.objects.get(tag="#secondday")

    def test_tag_signal(self):
        self.assertEqual(len(self.gym_tag.posts.all()), 2)
        self.assertIn(self.p1, self.gym_tag.posts.all())
        self.assertIn(self.p2, self.gym_tag.posts.all())

        self.assertEqual(len(self.flex_tag.posts.all()), 1)
        self.assertIn(self.p1, self.flex_tag.posts.all())
        self.assertNotIn(self.p2, self.flex_tag.posts.all())

        self.assertEqual(len(self.second_day_tag.posts.all()), 1)
        self.assertIn(self.p2, self.second_day_tag.posts.all())
        self.assertNotIn(self.p1, self.second_day_tag.posts.all())

    def test_get_hash_tags(self):
        self.assertEqual(self.p1.get_hash_tags(), ['#gym', '#flex'])
        self.assertEqual(len(self.p1.get_hash_tags()), 2)

    def test_delete_tag_reference_on_post_delete(self):
        self.p2.delete()
        self.assertEqual(len(self.gym_tag.posts.all()), 1)

    def test_adding_tags_when_post_is_updated(self):
        self.p2.content += " #bonushastag"
        self.p2.save()
        self.new_tag = Tag.objects.get(tag="#bonushastag")
        self.assertIn(self.p2, self.new_tag.posts.all())

    def test_delete_reference_when_tag_deleted_in_post_update(self):
        self.p2.content = self.p2.content.replace("#secondday", '')
        self.p2.save()
        self.removed_tag = Tag.objects.get(tag="#secondday")
        self.assertNotIn(self.p2, self.removed_tag.posts.all())


class TestResponding(TestCase):
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

    def test_valid_login(self):
        print self.u.email
        print self.u.password
        login = self.client.login(email=self.u.email, password='testpass')
        self.assertTrue(login)
