import factory
from django.contrib.auth.models import User

from .models import Collect, Reason


class UserFactory(factory.django.DjangoModelFactory):
    """Фабрика для создания экземпляров пользователя."""

    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.Sequence(lambda n: f'user{n}@example.com')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')


class CollectFactory(factory.django.DjangoModelFactory):
    """Фабрика для создания экземпляров группового денежного сбора."""

    class Meta:
        model = Collect

    author = factory.SubFactory(UserFactory)
    title = factory.Sequence(lambda n: f'Title{n}')
    reason = factory.Faker(
        'random_element',
        elements=[choice[0] for choice in Reason.choices])
    description = factory.Faker('paragraph')
    planned_amount = factory.Faker(
        'pydecimal',
        left_digits=6,
        right_digits=2,
        positive=True)
    cover_image = factory.django.ImageField(filename='example.jpg')
    finished_at = factory.Faker('date_time_this_year', after_now=True)
