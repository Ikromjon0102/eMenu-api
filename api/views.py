import logging
from django.middleware.csrf import get_token
from django.utils import timezone
from django.contrib.auth import login, logout
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import serializers, status
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from drf_yasg.utils import swagger_auto_schema
from cafes.models import Cafes
from users.models import TelegramProfile
from product.models import Category, Product
from product.serializers import (
    ProductSerializers,
    UpdateProductSerializers,
    CategorySerializers,
    UpdateCategorySerializers,
    ProductVariantSerializer
)
from cafes.serializers import CafesSerializers, UpdateCafesSerializer

# Logger setup
logger = logging.getLogger(__name__)

# Custom Exception classes
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

# Rate Limiting class
class LoginRateThrottle(UserRateThrottle):
    rate = '5/min'

# LoginAPIView class
# class LoginAPIView(APIView):
#     throttle_classes = [LoginRateThrottle]
#
#     def post(self, request):
#         serializer = OTPSerializer(data=request.data)
#         if serializer.is_valid():
#             otp_code = serializer.validated_data['otp_code']
#             try:
#                 profile = TelegramProfile.objects.get(
#                     otp_code=otp_code,
#                     otp_expiry__gt=timezone.now()
#                 )
#
#                 if profile.otp_expiry < timezone.now():
#                     logger.warning(f'OTP expired for user {profile.user.username}')
#                     raise OTPExpiredException()
#
#                 user = profile.user
#                 login(request, user)
#
#                 # Log successful login
#                 logger.info(f'User {user.username} logged in successfully with OTP {otp_code}')
#
#                 # Clear OTP
#                 profile.otp_code = None
#                 profile.otp_expiry = None
#                 profile.save()
#                 user = TelegramProfile.objects.get(user = request.user)
#
#                 csrf_token = get_token(request)
#                 response_data = {
#                     "detail": "Successfully logged in.",
#                     "csrf_token": csrf_token,
#                     'user': user
#                 }
#                 return Response(response_data, status=status.HTTP_200_OK)
#
#             except TelegramProfile.DoesNotExist:
#                 logger.warning(f'Failed login attempt with OTP {otp_code}')
#                 raise InvalidOTPException()
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from users.serializers import TelegramProfileSerializer
from django.middleware.csrf import get_token
from rest_framework import status
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)

class LoginAPIView(APIView):
    throttle_classes = [LoginRateThrottle]

    def post(self, request):
        serializer = OTPSerializer(data=request.data)
        if serializer.is_valid():
            otp_code = serializer.validated_data['otp_code']
            try:
                profile = TelegramProfile.objects.get(
                    otp_code=otp_code,
                    otp_expiry__gt=timezone.now()
                )

                if profile.otp_expiry < timezone.now():
                    logger.warning(f'OTP expired for user {profile.user.username}')
                    raise OTPExpiredException()

                user = profile.user
                login(request, user)

                # Log successful login
                logger.info(f'User {user.username} logged in successfully with OTP {otp_code}')

                # Clear OTP
                profile.otp_code = None
                profile.otp_expiry = None
                profile.save()

                # Foydalanuvchi ma'lumotlarini olish va serializer yordamida API response'ga qo'shish
                profile_serializer = TelegramProfileSerializer(profile)

                csrf_token = get_token(request)
                response_data = {
                    "detail": "Successfully logged in.",
                    "csrf_token": csrf_token,
                    'user': profile_serializer.data  # Bu yerda serializer'dan foydalanib user ma'lumotlarini qo'shish
                }
                return Response(response_data, status=status.HTTP_200_OK)

            except TelegramProfile.DoesNotExist:
                logger.warning(f'Failed login attempt with OTP {otp_code}')
                raise InvalidOTPException()

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# LogoutAPIView class
class LogoutAPIView(APIView):
    def post(self, request):
        logout(request)
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)

# Cafes Views
@swagger_auto_schema(method='GET')
@api_view(['GET'])
def cafes_list(request):
    cafes = Cafes.objects.all()
    serializer = CafesSerializers(cafes, many=True)
    return Response(serializer.data)

@swagger_auto_schema(method='GET')
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
        raise ValidationError('This data already exists')
    
    if serializer.is_valid():
        serializer.save()
        telegram_profile = TelegramProfile.objects.get(user=request.user)
        telegram_profile.has_cafe = True
        telegram_profile.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
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

# Category Views
@swagger_auto_schema(method='GET')
@api_view(['GET'])
def category_list(request):
    categories = Category.objects.all()
    serializer = CategorySerializers(categories, many=True)
    return Response(serializer.data)

@swagger_auto_schema(method='POST', request_body=CategorySerializers)
@api_view(['POST'])
def category_create(request):
    serializer = CategorySerializers(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='GET')
@api_view(['GET'])
def category_detail(request, pk):
    try:
        category = Category.objects.get(id=pk)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = CategorySerializers(category)
    return Response(serializer.data)

@swagger_auto_schema(method='PATCH', request_body=CategorySerializers)
@api_view(['PATCH'])
def category_update(request, pk):
    try:
        category = Category.objects.get(id=pk)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = CategorySerializers(category, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='DELETE')
@api_view(['DELETE'])
def category_delete(request, pk):
    try:
        category = Category.objects.get(id=pk)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    category.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# Product Views
@swagger_auto_schema(method='GET')
@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializers(products, many=True)
    return Response(serializer.data)

@swagger_auto_schema(method='POST', request_body=ProductSerializers)
@api_view(['POST'])
def product_create(request):
    serializer = ProductSerializers(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='GET')
@api_view(['GET'])
def product_detail(request, pk):
    try:
        product = Product.objects.get(id=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ProductSerializers(product)
    return Response(serializer.data)

@swagger_auto_schema(method='PATCH', request_body=ProductSerializers)
@api_view(['PATCH'])
def product_update(request, pk):
    try:
        product = Product.objects.get(id=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ProductSerializers(product, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='DELETE')
@api_view(['DELETE'])
def product_delete(request, pk):
    try:
        product = Product.objects.get(id=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    product.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# # Variant Views
# @swagger_auto_schema(method='GET')
# @api_view(['GET'])
# def variant_list(request):
#     variants = ProductVariant.objects.all()
#     serializer = VariantSerializer(variants, many=True)
#     return Response(serializer.data)

# @swagger_auto_schema(method='POST', request_body=VariantSerializer)
# @api_view(['POST'])
# def variant_create(request):
#     serializer = VariantSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @swagger_auto_schema(method='GET')
# @api_view(['GET'])
# def variant_detail(request, pk):
#     try:
#         variant = ProductVariant.objects.get(id=pk)
#     except Variant.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#     serializer = VariantSerializer(variant)
#     return Response(serializer.data)

# @swagger_auto_schema(method='PATCH', request_body=VariantSerializer)
# @api_view(['PATCH'])
# def variant_update(request, pk):
#     try:
#         variant = ProductVariant.objects.get(id=pk)
#     except Variant.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#     serializer = VariantSerializer(variant, data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @swagger_auto_schema(method='DELETE')
# @api_view(['DELETE'])
# def variant_delete(request, pk):
#     try:
#         variant = ProductVariant.objects.get(id=pk)
#     except Variant.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
    
#     variant.delete()
#     return Response(status=status.HTTP_204_NO_CONTENT)
