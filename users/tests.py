import random
from django.test import TestCase
from django.urls import reverse
from users.models import User, Organization, Queue


class QueueTestCase(TestCase):
    def setUp(self):
        # create org, users, and queue
        org_data = {
            'name': 'test_org',
            'email': 'test_mail@gmail.com',
            'phone_number': '+77472747681'
        }
        self.org = Organization.objects.create(**org_data)
        self.users = []
        for user in range(10):
            self.users.append(User.objects.create(
                username=user, phone_number=f'+777777777{user}'))
        self.queue = Queue.objects.create(org=self.org, description='')

    def test_adding_participants(self):
        for user in self.users:
            endpoint = reverse('add_to_queue', kwargs={
                               'queue_id': self.queue.id, 'user_id': user.id})
            self.client.post(endpoint)
        self.assertEqual(self.queue.participants.count(), len(self.users))
        # self.assertEqual(self.queue.count, len(self.users))
        # self.assertEqual(1, self.queue.current_pos)

    def test_processing_participant(self):
        for user in self.users:
            endpoint = reverse('add_to_queue', kwargs={
                               'queue_id': self.queue.id, 'user_id': user.id})
            self.client.post(endpoint)

        random_amount = random.randint(0, 10)
        endpoint = reverse('process_current_pos', kwargs={
            'queue_id': self.queue.id})
        for i in range(random_amount):
            self.client.post(endpoint)
        self.assertEqual(self.queue.participants.count(),
                         len(self.users) - random_amount)
