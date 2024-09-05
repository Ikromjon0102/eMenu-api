import logging
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth import login, logout
from .forms import OTPForm
from .models import TelegramProfile


logger = logging.getLogger(__name__)


def otp_login(request):
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            otp_code = form.cleaned_data['otp_code']
            try:
                profile = TelegramProfile.objects.get(otp_code=otp_code, otp_expiry__gt=timezone.now())

                if profile.otp_expiry < timezone.now():
                    logger.warning(f'OTP expired for user {profile.user.username}')
                    form.add_error('otp_code', 'OTP code has expired.')
                    return render(request, 'login1.html', {'form': form})

                user = profile.user
                login(request, user)

                # Log foydalanuvchi tizimga muvaffaqiyatli kirganligi haqida
                logger.info(f'User {user.username} logged in successfully with OTP {otp_code}')

                # OTP kodni o'chirib tashlash
                profile.otp_code = None
                profile.otp_expiry = None
                profile.save()

                return redirect('home')  # Kirgandan keyin yo'naltirish

            except TelegramProfile.DoesNotExist:
                logger.warning(f"Invalid or expired OTP code attempt: {otp_code}")
                form.add_error('otp_code', 'Invalid or expired OTP code.')
        else:
            logger.info("OTP form invalid.")
    else:
        form = OTPForm()

    return render(request, 'login1.html', {'form': form})

