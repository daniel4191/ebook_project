from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import SignupForm
from .models import User

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, '회원가입이 완료되었습니다.')
            login(request, user)
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'users/signup.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'users/profile.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        user.username = request.POST.get('username', user.username)
        if request.FILES.get('profile_image'):
            user.profile_image = request.FILES['profile_image']
        user.save()
        messages.success(request, '프로필이 수정되었습니다.')
        return redirect('users:profile')
    return render(request, 'users/edit_profile.html')
