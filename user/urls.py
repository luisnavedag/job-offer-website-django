from django.urls import path, include
from user.views import RegisterView, UserActivationView, ChangePasswordView, UserDetail
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('user/register/', RegisterView.as_view(), name='auth_register'),
    path('user/activate/', UserActivationView.as_view(), name='activate_register'),

    path('user/change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('user/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

    path('user/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('user/<str:pk>/', UserDetail.as_view(), name='user-detail'),
]