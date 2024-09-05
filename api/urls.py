from django.urls import path
from .views import LoginAPIView, LogoutAPIView
from . import views

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='api_login'),
    path('logout/', LogoutAPIView.as_view(), name='api_logout'),
    # Cafes URLs
    path('cafes/', views.cafes_list, name='cafes_list'),
    path('cafes/<uuid:pk>/', views.cafes_detail, name='cafes_detail'),
    path('cafes/create/', views.cafes_create, name='cafes_create'),
    path('cafes/update/<uuid:pk>/', views.cafes_update, name='cafes_update'),
    path('cafes/delete/<uuid:pk>/', views.cafes_delete, name='cafes_delete'),
    # Category URLs
    path('categories/', views.category_list, name='category-list'),
    path('categories/create/', views.category_create, name='category-create'),
    path('categories/<int:pk>/', views.category_detail, name='category-detail'),
    path('categories/<int:pk>/update/', views.category_update, name='category-update'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category-delete'),

    # Product URLs
    path('products/', views.product_list, name='product-list'),
    path('products/create/', views.product_create, name='product-create'),
    path('products/<int:pk>/', views.product_detail, name='product-detail'),
    path('products/<int:pk>/update/', views.product_update, name='product-update'),
    path('products/<int:pk>/delete/', views.product_delete, name='product-delete'),

    # Variant URLs
    # path('variants/', variant_list, name='variant-list'),
    # path('variants/create/', variant_create, name='variant-create'),
    # path('variants/<int:pk>/', variant_detail, name='variant-detail'),
    # path('variants/<int:pk>/update/', variant_update, name='variant-update'),
    # path('variants/<int:pk>/delete/', variant_delete, name='variant-delete'),

]


