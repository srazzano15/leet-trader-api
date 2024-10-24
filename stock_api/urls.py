from django.urls import path
from .views import StockDataView, StockMoversView

urlpatterns = [
    path('ticker/<str:ticker>/', StockDataView.as_view(), name='stock-data'),
    path('movers/', StockMoversView.as_view(), name='market-movers-data'),
]