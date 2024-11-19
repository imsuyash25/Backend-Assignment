from django.urls import path
from . import views

urlpatterns = [
    path('request-count/', views.RequestCountView.as_view()),
    path('request-count/reset/', views.RequestCountView.as_view())
]
