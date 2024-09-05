from rest_framework import serializers
from .models import TelegramProfile

class OTPSerializer(serializers.Serializer):
    otp_code = serializers.CharField(max_length=6)

class TelegramProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramProfile
        fields = ['id','telegram_id','full_name',"phone_number","has_cafe"]  # Qo'shimcha maydonlar kerak bo'lsa, bularni qo'shish mumkin
        # depth = 1  # Bu user ma'lumotlarini ham ko'rish uchun
