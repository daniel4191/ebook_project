from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.post_list, name='list'),
    path('<int:pk>/', views.post_detail, name='detail'),
    path('create/', views.post_create, name='create'),
    path('<int:pk>/edit/', views.post_update, name='update'),
    path('<int:pk>/delete/', views.post_delete, name='delete'),
    path('<int:pk>/comment/', views.comment_create, name='comment_create'),
    path('comment/<int:comment_pk>/delete/', views.comment_delete, name='comment_delete'),
]

