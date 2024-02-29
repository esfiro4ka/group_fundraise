import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import factory

from apps.collects.models import Collect
from apps.collects.factories import CollectFactory, UserFactory
from apps.payments.factories import PaymentFactory


class Command(BaseCommand):
    help = 'Creating mock data.'

    def add_arguments(self, parser):
        parser.add_argument(
            'number', type=int, help='Number of data to create')

    def create_users(self, number):
        UserFactory.create_batch(number)

    def create_collects(self, number):
        users = User.objects.all()
        CollectFactory.create_batch(
            number,
            author=factory.lazy_attribute(lambda _: random.choice(users)))

    def create_payments(self, number):
        users = User.objects.all()
        collects = Collect.objects.all()

        PaymentFactory.create_batch(
            number,
            donor=factory.lazy_attribute(lambda _: random.choice(users)),
            collect=factory.lazy_attribute(lambda _: random.choice(collects)))

    def handle(self, *args, **options):
        number = options['number']

        try:
            self.create_users(number)
            self.create_collects(number)
            self.create_payments(number)

            self.stdout.write(self.style.SUCCESS(
                'Test data created successfully!'))
        except Exception as exp:
            self.stdout.write(self.style.ERROR('Error: %s' % exp))
