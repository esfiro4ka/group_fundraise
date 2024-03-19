import random
from decimal import Decimal

import factory

from apps.collects.factories import CollectFactory, UserFactory

from .models import Payment, Type


class PaymentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Payment

    collect = factory.SubFactory(CollectFactory)
    donor = factory.SubFactory(UserFactory)
    type = factory.Faker(
        'random_element',
        elements=[choice[0] for choice in Type.choices])
    amount = factory.LazyFunction(
        lambda: Decimal(
            random.lognormvariate(0.5, 3) * 100).quantize(Decimal('.01')))
