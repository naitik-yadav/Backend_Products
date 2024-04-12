from django.db import models
from django_base64field.fields import Base64Field
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken
from channels.layers import get_channel_layer
import asyncio
from django.core.serializers import serialize

class Nike(models.Model):
    ShoeName = models.CharField(max_length=80)
    ShoeNumber = models.IntegerField()
    ShoeType = models.CharField(max_length=225)
    Gender = models.CharField(max_length=225)
    Price = models.DecimalField(max_digits=10, decimal_places=2)
    images = models.FileField(validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
                                      upload_to='images/', default='path/to/default/image.png' )

    def get_serialized_data(self):
        return serialize('json', [self])


    async def notify_consumers(self):
        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            "nike_updates_group",
            {"type": "nike.update", "new_shoe_data": self.get_serialized_data()}
        )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        asyncio.run(self.notify_consumers())




class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.username

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return{
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }