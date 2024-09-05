
import logging
from django.middleware.csrf import get_token

from django.utils import timezone
from django.contrib.auth import login, logout
from rest_framework import serializers, status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from users.serializers import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from users.models import TelegramProfile, Cafes
from .serializers import *
# Logger o'rnatish
logger = logging.getLogger(__name__)

# Custom Exception klasslari
class OTPExpiredException(APIException):
    status_code = 400
    default_detail = 'OTP code has expired.'
    default_code = 'otp_expired'

class InvalidOTPException(APIException):
    status_code = 400
    default_detail = 'Invalid OTP code.'
    default_code = 'invalid_otp'

# OTP Serializer
class OTPSerializer(serializers.Serializer):
    otp_code = serializers.CharField(max_length=6)

# Rate Limiting sinfi
class LoginRateThrottle(UserRateThrottle):
    rate = '5/min'


# LoginAPIView klassi
class LoginAPIView(APIView):
    throttle_classes = [LoginRateThrottle]

    def post(self, request):
        serializer = OTPSerializer(data=request.data)
        if serializer.is_valid():
            otp_code = serializer.validated_data['otp_code']
            try:
                profile = TelegramProfile.objects.get(otp_code=otp_code, otp_expiry__gt=timezone.now())

                if profile.otp_expiry < timezone.now():
                    logger.warning(f'OTP expired for user {profile.user.username}')
                    raise OTPExpiredException()

                user = profile.user
                login(request, user)

                # Log foydalanuvchi tizimga muvaffaqiyatli kirganligi haqida
                logger.info(f'User {user.username} logged in successfully with OTP {otp_code}')

                # OTP kodni o'chirib tashlash
                profile.otp_code = None
                profile.otp_expiry = None
                profile.save()
                csrf_token = get_token(request)

                response_data = {
                    "detail": "Successfully logged in.",
                    "csrf_token": csrf_token
                }

                return Response(response_data, status=status.HTTP_200_OK)

            except TelegramProfile.DoesNotExist:
                logger.warning(f'Failed login attempt with OTP {otp_code}')
                raise InvalidOTPException()

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    def post(self, request):
        # Foydalanuvchini tizimdan chiqarish
        logout(request)
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)

@swagger_auto_schema(methods='GET')
@api_view(['GET'])
def cafes_list(request):
    if request.method == 'GET':
        cafes = Cafes.objects.all()
        serializer = CafesSerializers(cafes, many=True)
        return Response(serializer.data)

@swagger_auto_schema(methods='GET')
@api_view(['GET'])
def cafes_detail(request, pk):
    try:
        cafe = Cafes.objects.get(id=pk)
    except Cafes.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = CafesSerializers(cafe)
    return Response(serializer.data)

@swagger_auto_schema(method='POST', request_body=CafesSerializers)
@api_view(['POST'])
def cafes_create(request):
    serializer = CafesSerializers(data=request.data)
    if Cafes.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='PATCH', request_body=UpdateCafesSerializer)
@api_view(['PATCH'])
def cafes_update(request, pk):
    try:
        cafe = Cafes.objects.get(id=pk)
    except Cafes.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = UpdateCafesSerializer(instance=cafe, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='DELETE')
@api_view(['DELETE'])
def cafes_delete(request, pk):
    try:
        cafe = Cafes.objects.get(id=pk)
    except Cafes.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    cafe.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)