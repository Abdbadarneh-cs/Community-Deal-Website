from django.shortcuts import redirect
from django.urls import reverse
from django_otp.plugins.otp_totp.models import TOTPDevice

class OTPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            device = TOTPDevice.objects.filter(user=request.user, confirmed=True).first()
            if device and not hasattr(request, 'otp_device'):
                if request.path != reverse('verify_otp'):
                    return redirect('verify_otp')
        return self.get_response(request)
