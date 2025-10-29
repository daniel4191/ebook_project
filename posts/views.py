from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Post, Comment
from .forms import PostForm, CommentForm

def post_list(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    return render(request, 'posts/list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.increment_view_count()
    comments = post.comments.all()
    
    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, '댓글이 등록되었습니다.')
            return redirect('posts:detail', pk=post.pk)
    else:
        form = CommentForm()
    
    return render(request, 'posts/detail.html', {
        'post': post,
        'comments': comments,
        'form': form
    })

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, '포스트가 작성되었습니다.')
            return redirect('posts:detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'posts/create.html', {'form': form})

@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        messages.error(request, '수정 권한이 없습니다.')
        return redirect('posts:detail', pk=post.pk)
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, '포스트가 수정되었습니다.')
            return redirect('posts:detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/update.html', {'form': form, 'post': post})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        messages.error(request, '삭제 권한이 없습니다.')
        return redirect('posts:detail', pk=post.pk)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, '포스트가 삭제되었습니다.')
        return redirect('posts:list')
    
    return render(request, 'posts/delete_confirm.html', {'post': post})

@login_required
def comment_create(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, '댓글이 등록되었습니다.')
    return redirect('posts:detail', pk=post.pk)

@login_required
def comment_delete(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if comment.author != request.user:
        messages.error(request, '삭제 권한이 없습니다.')
        return redirect('posts:detail', pk=comment.post.pk)
    
    if request.method == 'POST':
        comment.delete()
        messages.success(request, '댓글이 삭제되었습니다.')
    
    return redirect('posts:detail', pk=comment.post.pk)
