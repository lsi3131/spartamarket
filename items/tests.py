from django.test import TestCase
from .models import *
from accounts.models import User


# Create your tests here.
class ItemTestCase(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(username='user', password='password')

    def test_create_item(self):
        item = Item.objects.create(title='title', content='content', price=1000, user=self.test_user)
        self.assertIsNotNone(item)

    def test_create_hashtag(self):
        item1 = Item.objects.create(title='item1', content='content', price=1000, user=self.test_user)
        item2 = Item.objects.create(title='item2', content='content', price=1000, user=self.test_user)
        hashtag1 = HashTag.objects.create(name='tag1')
        hashtag2 = HashTag.objects.create(name='tag2')

        item1.save()
        item2.save()
        hashtag1.save()
        hashtag2.save()

        tagged_item1_1 = TaggedItem.objects.create(item=item1, tag=hashtag1)
        tagged_item1_2 = TaggedItem.objects.create(item=item1, tag=hashtag2)
        tagged_item2_1 = TaggedItem.objects.create(item=item2, tag=hashtag1)

        tagged_item1_1.save()
        tagged_item1_2.save()
        tagged_item2_1.save()

        tagged_items = TaggedItem.objects.all()
        self.assertEqual(3, tagged_items.count())
        self.assertEqual(2, TaggedItem.objects.filter(item=item1).count())
        self.assertEqual(1, TaggedItem.objects.filter(item=item2).count())
