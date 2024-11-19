from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterUserAPIView.as_view()),
    path('login/', views.LoginUserAPIView.as_view()),
    path('movies/', views.ListMoviesAPIView.as_view(), name='movie-list'),
    path('collection/', views.CollectionListCreateView.as_view()),
    path('collection/<slug:pk>/', views.CollectionManageView.as_view())
]
