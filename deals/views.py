from django.shortcuts import render , redirect
from .models import Deal
from .forms import UserRegisterForm, DealForm , UserProfileForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model



def deal_list(request):
    deals = Deal.objects.filter(is_approved=True).order_by('-created_at')
    return render(request, 'deals/index.html',{'deals':deals})

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('deal_list')
    else:
        form = UserRegisterForm()
    return render(request, 'deals/register.html',{'form':form})


User = get_user_model()

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            device = TOTPDevice.objects.filter(user=user, confirmed=True).first()
            if device:
                request.session['pre_otp_user_id'] = user.id
                logout(request)  
                return redirect('verify_otp')
            else:
                login(request, user)
                return redirect('deal_list')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'deals/login.html')



def logout_view(request):
    logout(request)
    return redirect('login')


def enable_otp(request):
    user = request.user
    device, created = TOTPDevice.objects.get_or_create(user=user, name='default')
    if not device.confirmed:
        qr_code_url = device.config_url
        return render(request, 'deals/enable_otp.html', {'qr_code_url': qr_code_url})
    
    return redirect ('deal_list')



def verify_otp(request):
    if request.method == 'POST':
        code = request.POST.get('token')
        user_id = request.session.get('pre_otp_user_id')

        if not user_id:
            messages.error(request, 'Session expired. Please login again.')
            return redirect('login')

        user = User.objects.get(id=user_id)
        device = TOTPDevice.objects.filter(user=user, confirmed=True).first()

        if device and device.verify_token(code):
            login(request, user) 
            del request.session['pre_otp_user_id']
            return redirect('deal_list')
        else:
            messages.error(request, 'Invalid OTP code')

    return render(request, 'deals/verify_otp.html')


def add_deal_view(request):
    if request.method == 'POST':
        form = DealForm(request.POST, request.FILES)
        if form.is_valid():
            deal = form.save(commit=False)
            deal.owner = request.user
            deal.save()
            return redirect('deal_list')
    else:
        form = DealForm()
    return render(request,'deals/add_deal.html', {'form': form} )


@login_required
def profile_detail_view(request):
    user=request.user
    deals = Deal.objects.filter(owner=user)
    return render(request,'deals/profile_detail.html',{'user':user,'deals':deals})


@login_required
def profile_view(request):
    user = request.user

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user)
    return render(request, 'deals/profile.html', {'form': form})


