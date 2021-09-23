from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('post/<slug:slug>/', views.show_post, name='post'),
]
