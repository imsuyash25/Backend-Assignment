from django.urls import path
from . import views

urlpatterns = [
    path('movies/', views.ListMoviesAPIView.as_view(), name='movie-list'),
    path('collection/', views.CollectionListCreateView.as_view()),
    path('collection/<slug:pk>/', views.CollectionManageView.as_view())
]
