from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import otp_login



urlpatterns = [
    path('login/', otp_login, name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),

]


