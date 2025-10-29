from django.contrib import admin
from .models import Ebook, Purchase, Review, Bookmark

@admin.register(Ebook)
class EbookAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'total_rating', 'review_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['title', 'description']
    ordering = ['-created_at']

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['user', 'ebook', 'payment_method', 'purchase_price', 'is_completed', 'purchased_at']
    list_filter = ['is_completed', 'payment_method', 'purchased_at']
    search_fields = ['user__email', 'ebook__title']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['ebook', 'author', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['content']

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ['user', 'ebook', 'page', 'created_at']
    list_filter = ['created_at']
    search_fields = ['note']

