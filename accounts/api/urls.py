from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterUserAPIView.as_view()),
    path('login/', views.LoginUserAPIView.as_view()),
    path('request-count/', views.RequestCountView.as_view()),
    path('request-count/reset/', views.RequestCountResetView.as_view())
]
