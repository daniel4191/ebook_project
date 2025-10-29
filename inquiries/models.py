from django.db import models
from users.models import User

class Inquiry(models.Model):
    """
    문의 모델
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='inquiries',
        verbose_name='사용자'
    )
    title = models.CharField(
        max_length=200,
        verbose_name='제목'
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
    is_read = models.BooleanField(
        default=False,
        verbose_name='읽음 여부'
    )
    
    class Meta:
        verbose_name = '문의'
        verbose_name_plural = '문의들'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
