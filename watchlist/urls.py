from django.urls import path
from . import views

urlpatterns = [
    path('', views.watchlist_list, name='watchlist_list'),
    path('<int:pk>/', views.watchlist_detail, name='watchlist_detail'),
    path('<int:pk>/add-assets/', views.add_assets_to_watchlist, name='add-assets'),
]