from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from django.urls import reverse
from posts.models import Post, Tag
MyUser = get_user_model()


class TestTrending(TestCase):
    client = Client()

    def setUp(self):
        self.u = MyUser.objects.create_user(username='dasde',
                                            email='test@gmail.com',
                                            first_name="Simo", last_name='Rolev')
        self.u.set_password('testpass')
        self.u.save()
        self.login = self.client.login(email=self.u.email, password='testpass')

        self.p1 = Post(posted_by=self.u, content="Working out! #gym #flex")
        self.p1.save()
        self.p2 = Post(posted_by=self.u, content="Working out! #gym #flex")
        self.p2.save()
        self.p3 = Post(posted_by=self.u, content="Working out! #day #money")
        self.p3.save()
        self.p4 = Post(posted_by=self.u, content="Working out! #day #money")
        self.p4.save()
        self.p5 = Post(posted_by=self.u, content="Day two! #party #sleep")
        self.p5.save()
        self.p5 = Post(posted_by=self.u, content="Day two! #party #done")
        self.p5.save()

        self.gym_tag = Tag.objects.get(tag="#gym")
        self.flex_tag = Tag.objects.get(tag="#flex")
        self.day_tag = Tag.objects.get(tag="#day")
        self.money_tag = Tag.objects.get(tag="#money")
        self.party_tag = Tag.objects.get(tag="#party")
        self.sleep_tag = Tag.objects.get(tag="#sleep")
        self.done_tag = Tag.objects.get(tag="#done")

        self.assertTrue(self.login)
        self.response = self.client.get(reverse('posts:trending'))
        self.full_content = self.response.content

    def test_trending_access(self):
        self.assertIn("Trending tags in latest posts", self.full_content)
        self.assertEqual(self.response.status_code, 200)

    def test_trending_top(self):
        # The top tags must be gym, flex, day, money and party
        gym_tag_page = reverse('posts:tag', kwargs={'tag': 'gym'})
        gym_html = '<li id="tag{}"> <a href="{}">Tag #gym</a> - Found in 2 posts </li>'.format(self.gym_tag.id, gym_tag_page)
        self.assertIn(gym_html, self.full_content)

        flex_tag_page = reverse('posts:tag', kwargs={'tag': 'flex'})
        flex_html = '<li id="tag{}"> <a href="{}">Tag #flex</a> - Found in 2 posts </li>'.format(self.flex_tag.id, flex_tag_page)
        self.assertIn(flex_html, self.full_content)

        day_tag_page = reverse('posts:tag', kwargs={'tag': 'day'})
        day_html = '<li id="tag{}"> <a href="{}">Tag #day</a> - Found in 2 posts </li>'.format(self.day_tag.id, day_tag_page)
        self.assertIn(day_html, self.full_content)

        money_tag_page = reverse('posts:tag', kwargs={'tag': 'money'})
        money_html = '<li id="tag{}"> <a href="{}">Tag #money</a> - Found in 2 posts </li>'.format(self.money_tag.id, money_tag_page)
        self.assertIn(money_html, self.full_content)

        party_tag_page = reverse('posts:tag', kwargs={'tag': 'party'})
        party_html = '<li id="tag{}"> <a href="{}">Tag #party</a> - Found in 2 posts </li>'.format(self.party_tag.id, party_tag_page)
        self.assertIn(party_html, self.full_content)

        # Tags the should not be in the trending page
        sleep_tag_page = reverse('posts:tag', kwargs={'tag': 'sleep'})
        sleep_html = '<li id="tag{}"> <a href="{}">Tag #sleep</a> - Found in 2 posts </li>'.format(self.sleep_tag.id, sleep_tag_page)
        self.assertNotIn(sleep_html, self.full_content)

        done_tag_page = reverse('posts:tag', kwargs={'tag': 'done'})
        done_html = '<li id="tag{}"> <a href="{}">Tag #done</a> - Found in 2 posts </li>'.format(self.done_tag.id, done_tag_page)
        self.assertNotIn(done_html, self.full_content)
