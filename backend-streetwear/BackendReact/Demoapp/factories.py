import factory
from Demoapp.models import Nike, User


class NikeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Nike

    ShoeName = factory.Faker('name')
    ShoeNumber = factory.Faker('random_int')
    ShoeType = factory.Faker('text')
    Gender = factory.Faker('text')
    Price = factory.Faker('random_int')
    images = factory.django.FileField(filename='test_image.jpg')


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', 'testpassword')
    is_staff = True
    is_active = True