from django.db import models
from users.models import TelegramProfile
import uuid
# Create your models here.

class Cafes(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, null=False, editable=False)
    owner_id = models.OneToOneField(TelegramProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=150,null=True, blank=True)
    location = models.CharField(max_length=150, null=True, blank=True)
    description = models.CharField(max_length=150, null=True, blank=True)
    phone_number = models.CharField(max_length=150, null=True, blank=True)
    logo = models.ImageField(default='products/default.png', upload_to='products')
    start_time = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name