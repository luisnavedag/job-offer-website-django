from django.urls import path, include

from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'employer', views.EmployerDetail, basename='employer')

urlpatterns = [
    path('subscription/', views.SubscriptionCreate.as_view(), name='subscription'),
    path('subscriptions/', views.SubscriptionList.as_view(), name='subscriptions'),
    path('', include(router.urls)),
]

