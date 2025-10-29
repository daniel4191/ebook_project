"""
복사/붙여넣기 추적 모듈
"""
from django.db import models
from .models import Ebook

class CopyTracking(models.Model):
    """
    복사/붙여넣기 추적 모델
    """
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        verbose_name='사용자'
    )
    ebook = models.ForeignKey(
        Ebook,
        on_delete=models.CASCADE,
        verbose_name='전자책'
    )
    content = models.TextField(
        verbose_name='복사된 내용'
    )
    copied_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='복사 시각'
    )
    
    class Meta:
        verbose_name = '복사 추적'
        verbose_name_plural = '복사 추적들'
    
    def __str__(self):
        return f'{self.user.email} - {self.ebook.title} - {self.copied_at}'

