import random
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.utils import timezone
from datetime import timedelta
import secrets
from django.db import models
from django.contrib.auth.models import User


class TelegramProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telegram_id = models.BigIntegerField(unique=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)  # Yangilangan qator
    phone_number = models.CharField(max_length=15, null=True, blank=True)  # Yangilangan qator
    otp_code = models.CharField(max_length=6, null=True, blank=True)  # 6 xonali OTP kod
    otp_expiry = models.DateTimeField(null=True, blank=True)
    has_cafe = models.BooleanField(default=False)

    def generate_otp_code(self):
        self.otp_code = f"{secrets.randbelow(1000000):06}"  # 6 xonali raqamli kod
        self.otp_expiry = timezone.now() + timedelta(minutes=1)  # 1 daqiqa amal qilish muddati
        self.save()

    def is_otp_valid(self):
        if self.otp_expiry and timezone.now() < self.otp_expiry:
            return True
        return False

    def __str__(self):
        return str(self.user)
