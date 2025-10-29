from django.urls import path
from . import views

app_name = 'inquiries'

urlpatterns = [
    path('', views.inquiry_create, name='create'),
]

