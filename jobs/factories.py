from django.contrib.auth import get_user_model

from factory.django import DjangoModelFactory
from factory.faker import Faker

from .models import Post, Company


class CompanyFactory(DjangoModelFactory):
    class Meta:
        model = Company

    name = Faker("company")
    country = Faker("country")
    region = Faker("city")


class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post

    title = Faker("name")
    position = Faker("job")
    compensation = Faker("pyint")
    technology = Faker("catch_phrase")
    description = Faker("text")


class UserFactory(DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = Faker("first_name")
    password = Faker("last_name")
