
from django.urls import path
from product.views import ProductView, ProductDetailView, create_product, product_detail

urlpatterns = [
    path('all/', ProductView.as_view(), name='product_list'),
    # path('<int:product_id>', ProductDetailView.as_view(), name='product'),
    path('<int:product_id>', product_detail, name='product'),
    # path('add/', AddProductView.as_view(), name='add_product'),
    path('create-product/', create_product, name='create_product'),


]