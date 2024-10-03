from django.urls import path
from .views import StockDataView

urlpatterns = [
    path('<str:ticker>/', StockDataView.as_view(), name='get-stock-data'),
]