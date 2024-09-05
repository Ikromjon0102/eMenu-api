# users/forms.py

from django import forms

class OTPForm(forms.Form):
    otp_code = forms.CharField(max_length=6, label="Enter your OTP code")
