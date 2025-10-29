from django.urls import path
from django.shortcuts import render
from posts.models import Post
from ebooks.models import Ebook

def home(request):
    # 최신글 3개
    latest_posts = Post.objects.all()[:3]
    
    # 최신 전자책 3개
    latest_ebooks = Ebook.objects.all().order_by('-created_at')[:3]
    
    return render(request, 'home.html', {
        'latest_posts': latest_posts,
        'latest_ebooks': latest_ebooks
    })

urlpatterns = [
    path('', home, name='home'),
]

