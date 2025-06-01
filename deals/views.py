from django.shortcuts import render, redirect, get_object_or_404
from .models import Deal, Like , Comment,Follow
from .forms import UserRegisterForm, DealForm, UserProfileForm , DealFilterForm , CommentForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.contrib.auth.decorators import login_required




@login_required
def deal_list(request):
    deals = Deal.objects.filter(is_approved=True).order_by('-created_at')
    form = DealFilterForm(request.GET or None)
    
    if form.is_valid():
        search = form.cleaned_data.get('search')
        category = form.cleaned_data.get('category')
        sort_by = form.cleaned_data.get('sort_by')

        if search:
            deals = deals.filter(title__icontains=search)  
        if category:
            deals = deals.filter(category=category)       
        if sort_by:
            deals = deals.order_by(sort_by)
    comment_forms = {deal.id: CommentForm() for deal in deals}

  
    if request.method == 'POST':
        deal_id = request.POST.get('deal_id')
        deal = Deal.objects.get(id=deal_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.deal = deal
            comment.save()
            return redirect('deal_list')

    return render(request, 'deals/index.html', {'deals': deals,'form': form,'comment_forms': comment_forms,})
               







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

@login_required
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


@login_required
def toggle_like(request, deal_id):
    deal = get_object_or_404(Deal, id=deal_id)
    like, created = Like.objects.get_or_create(user=request.user, deal=deal)

    if not created:
        like.delete()
    return redirect('deal_list')

@login_required
def deal_detail(request, deal_id):
    deal = get_object_or_404(Deal, id=deal_id)
    comments = deal.comments.all().order_by('created_at')
    form = CommentForm()
    editing_comment = None

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'add':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.deal = deal
                comment.save()
                return redirect('deal_detail', deal_id=deal.id)

        elif action == 'edit':
            comment_id = request.POST.get('comment_id')
            comment = get_object_or_404(Comment, id=comment_id, user=request.user)
            editing_comment = comment
            form = CommentForm(instance=comment)  

        elif action == 'update':
            comment_id = request.POST.get('comment_id')
            comment = get_object_or_404(Comment, id=comment_id, user=request.user)
            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                form.save()
                return redirect('deal_detail', deal_id=deal.id)
            else:
                editing_comment = comment

        elif action == 'delete':
            comment_id = request.POST.get('comment_id')
            comment = get_object_or_404(Comment, id=comment_id, user=request.user)
            comment.delete()
            return redirect('deal_detail', deal_id=deal.id)

    return render(request, 'deals/deal_detail.html', {'deal': deal, 'form': form, 'comments': comments,'editing_comment': editing_comment })

@login_required
def profile_detail_view(request, user_id=None):
    if user_id:
        user_profile = get_object_or_404(User, id=user_id)
    else:
        user_profile = request.user

    deals = Deal.objects.filter(owner=user_profile)
    is_following = False
    if user_profile != request.user:
        is_following = Follow.objects.filter(follower=request.user, following=user_profile).exists()


    followers = Follow.objects.filter(following=user_profile)
    following = Follow.objects.filter(follower=user_profile)

    return render(request, 'deals/profile_detail.html', {'user_profile': user_profile,'deals': deals,'is_following': is_following,
        'followers': followers,
        'following': following,
        'followers_count': followers.count(),
        'following_count': following.count(),
    })



@login_required
def user_profile_view(request, user_id):
    user_profile = get_object_or_404(User, id=user_id)

    # cant follow your self
    if user_profile == request.user:
        is_following = False
    else:
        is_following = Follow.objects.filter(follower=request.user, following=user_profile).exists()

        if request.method == 'POST':
            if is_following:
                Follow.objects.filter(follower=request.user, following=user_profile).delete()
                is_following = False
            else:
                Follow.objects.create(follower=request.user, following=user_profile)
                is_following = True

            return redirect('user-profile', user_id=user_id)  

    user_deals = Deal.objects.filter(owner=user_profile, is_approved=True)

    return render(request, 'deals/user_profile.html', { 'user_profile': user_profile, 'is_following': is_following, 'deals': user_deals, })
