from django.test import TestCase
from .models import Post, Tag
from django.contrib.auth import get_user_model

MyUser = get_user_model()


class TestPosts(TestCase):

    def setUp(self):
        self.u = MyUser(5, first_name="Simo")
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

    def test_tag_is_deleted_when_all_references_are_deleted(self):
        self.p1.delete()
        self.p2.delete()
        print self.gym_tag.posts.all()
        self.assertIsNone(self.gym_tag)
