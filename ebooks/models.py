from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from users.models import User
from decimal import Decimal

class Ebook(models.Model):
    """
    전자책 모델
    """
    title = models.CharField(
        max_length=200,
        verbose_name='제목'
    )
    description = models.TextField(
        verbose_name='설명'
    )
    thumbnail = models.ImageField(
        upload_to='ebook_thumbnails/',
        null=True,
        blank=True,
        verbose_name='썸네일'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='가격'
    )
    total_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.00,
        verbose_name='총 평점'
    )
    review_count = models.IntegerField(
        default=0,
        verbose_name='리뷰 수'
    )
    ebook_file = models.FileField(
        upload_to='ebooks/',
        verbose_name='전자책 파일'
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
        verbose_name = '전자책'
        verbose_name_plural = '전자책들'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('ebooks:detail', kwargs={'pk': self.pk})
    
    def update_rating(self):
        """평균 평점 계산"""
        reviews = self.reviews.all()
        if reviews.exists():
            self.total_rating = reviews.aggregate(models.Avg('rating'))['rating__avg']
            self.review_count = reviews.count()
            self.save(update_fields=['total_rating', 'review_count'])


class Purchase(models.Model):
    """
    구매 모델
    """
    PAYMENT_METHOD_CHOICES = [
        ('kakao', '카카오페이'),
        ('naver', '네이버페이'),
        ('paypal', '페이팔'),
        ('cart', '장바구니'),
        ('direct', '바로결제'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='purchases',
        verbose_name='사용자'
    )
    ebook = models.ForeignKey(
        Ebook,
        on_delete=models.CASCADE,
        related_name='purchases',
        verbose_name='전자책'
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        verbose_name='결제 방법'
    )
    purchase_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='구매 가격'
    )
    is_completed = models.BooleanField(
        default=False,
        verbose_name='결제 완료'
    )
    purchased_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='구매일'
    )
    
    class Meta:
        verbose_name = '구매'
        verbose_name_plural = '구매들'
        ordering = ['-purchased_at']
        unique_together = ['user', 'ebook']
    
    def __str__(self):
        return f'{self.user.email} - {self.ebook.title}'


class Review(models.Model):
    """
    전자책 리뷰 모델
    """
    ebook = models.ForeignKey(
        Ebook,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='전자책'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='작성자'
    )
    purchase = models.ForeignKey(
        Purchase,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='구매'
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='평점'
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
        verbose_name = '리뷰'
        verbose_name_plural = '리뷰들'
        ordering = ['-created_at']
        unique_together = ['ebook', 'author']
    
    def __str__(self):
        return f'{self.author.email} - {self.ebook.title} - {self.rating}점'


class Bookmark(models.Model):
    """
    책갈피 모델
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookmarks',
        verbose_name='사용자'
    )
    ebook = models.ForeignKey(
        Ebook,
        on_delete=models.CASCADE,
        related_name='bookmarks',
        verbose_name='전자책'
    )
    page = models.IntegerField(
        verbose_name='페이지'
    )
    note = models.TextField(
        blank=True,
        verbose_name='메모'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='생성일'
    )
    
    class Meta:
        verbose_name = '책갈피'
        verbose_name_plural = '책갈피들'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.user.email} - {self.ebook.title} - {self.page}페이지'
