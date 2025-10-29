from django.urls import path
from . import views

app_name = 'ebooks'

urlpatterns = [
    path('', views.ebook_list, name='list'),
    path('<int:pk>/', views.ebook_detail, name='detail'),
    path('<int:pk>/purchase/', views.ebook_purchase, name='purchase'),
    path('<int:pk>/review/', views.ebook_review_create, name='review_create'),
    path('my-books/', views.my_ebooks, name='my_ebooks'),
    path('viewer/<int:pk>/', views.ebook_viewer, name='viewer'),
]

