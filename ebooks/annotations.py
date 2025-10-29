"""
필기/하이라이트 모델
"""
from django.db import models

class Annotation(models.Model):
    """
    필기/하이라이트 모델
    """
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='annotations',
        verbose_name='사용자'
    )
    ebook = models.ForeignKey(
        'ebooks.Ebook',
        on_delete=models.CASCADE,
        related_name='annotations',
        verbose_name='전자책'
    )
    page = models.IntegerField(
        verbose_name='페이지'
    )
    x = models.FloatField(
        verbose_name='X 좌표'
    )
    y = models.FloatField(
        verbose_name='Y 좌표'
    )
    content = models.TextField(
        blank=True,
        verbose_name='내용'
    )
    annotation_type = models.CharField(
        max_length=20,
        choices=[
            ('highlight', '하이라이트'),
            ('note', '메모'),
            ('drawing', '그림'),
        ],
        default='highlight',
        verbose_name='유형'
    )
    color = models.CharField(
        max_length=7,
        default='#FFD700',
        verbose_name='색상'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='생성일'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='수정일'
    )
    
    class Meta:
        verbose_name = '어노테이션'
        verbose_name_plural = '어노테이션들'
    
    def __str__(self):
        return f'{self.user.email} - {self.ebook.title} - {self.page}페이지'

