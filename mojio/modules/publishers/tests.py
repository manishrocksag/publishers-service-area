from unittest import TestCase

from .models import Publisher


class PublishersModelsTest(TestCase):
    def setUp(self):
        Publisher.objects.all().delete()
        self.publisher = Publisher.objects.create(
            publisher_id='aBdcide',
            name='test',
            email='test@test.com',
            phone_no='XXXX-XXX-XX',
            language='EN',
            currency='USD'
        )

    def tearDown(self):
        self.publisher.delete()

    def test_is_active(self):
        self.publisher.is_active = True
        self.publisher.save()

        self.assertEqual(self.publisher.is_active, True)

    def test_get_publishers_list(self):
        publishers_list = Publisher.objects.filter(is_active=True)
        self.assertEqual(len(publishers_list), 1)

