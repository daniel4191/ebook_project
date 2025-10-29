from django.db import models
from django.urls import reverse
from django.utils import timezone
from users.models import User

class Post(models.Model):
    """
    포스트 모델
    """
    title = models.CharField(
        max_length=200,
        verbose_name='제목'
    )
    content = models.TextField(
        verbose_name='내용'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='작성자'
    )
    view_count = models.IntegerField(
        default=0,
        verbose_name='조회수'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='작성일'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='수정일'
    )
    
    class Meta:
        verbose_name = '포스트'
        verbose_name_plural = '포스트들'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={'pk': self.pk})
    
    def increment_view_count(self):
        self.view_count += 1
        self.save(update_fields=['view_count'])


class Comment(models.Model):
    """
    포스트 댓글 모델
    """
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='포스트'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='작성자'
    )
    content = models.TextField(
        verbose_name='내용'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='작성일'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='수정일'
    )
    
    class Meta:
        verbose_name = '댓글'
        verbose_name_plural = '댓글들'
        ordering = ['created_at']
    
    def __str__(self):
        return f'{self.author.email} - {self.post.title}'
