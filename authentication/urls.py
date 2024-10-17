from django.urls import path
from .views import RegisterUserView, LoginView, UserView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('user/', UserView.as_view(), name='user'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]
