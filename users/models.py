from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from PIL import Image
import os

class User(AbstractUser):
    """
    커스텀 User 모델
    """
    email = models.EmailField(
        unique=True,
        verbose_name='이메일'
    )
    profile_image = models.ImageField(
        upload_to='profile_images/',
        null=True,
        blank=True,
        verbose_name='프로필 이미지',
        default='profile_images/default_avatar.png'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='가입일'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='수정일'
    )
    is_email_verified = models.BooleanField(
        default=False,
        verbose_name='이메일 인증 여부'
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = '사용자들'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        if self.profile_image:
            img = Image.open(self.profile_image.path)
            
            # 이미지 크기 조정 (최대 300x300)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.profile_image.path)
