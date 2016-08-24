from django.test import TestCase
from .models import Post, Tag
from django.contrib.auth import get_user_model

MyUser = get_user_model()


class TestPosts(TestCase):

    def setUp(self):
        self.u = MyUser(5, email='test@gmail.com', password='testpass',first_name="Simo")
        self.u.save()
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

