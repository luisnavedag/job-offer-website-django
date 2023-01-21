from django.urls import path, include
from user.views import RegisterView, UserActivationView, ChangePasswordView, UserDetail
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('activate/', UserActivationView.as_view(), name='activate_register'),

    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('<str:pk>/', UserDetail.as_view(), name='user-detail'),
]