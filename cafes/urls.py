from django.urls import path
from . import views
from .views import LoginAPIView, LogoutAPIView, Cafes


urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='api_login'),
    path('logout/', LogoutAPIView.as_view(), name='api_logout'),
    path('cafes/', views.cafes_list, name='cafes_list'),
    path('cafes/<uuid:pk>/', views.cafes_detail, name='cafes_detail'),
    path('cafes/create/', views.cafes_create, name='cafes_create'),
    path('cafes/update/<uuid:pk>/', views.cafes_update, name='cafes_update'),
    path('cafes/delete/<uuid:pk>/', views.cafes_delete, name='cafes_delete'),
]
