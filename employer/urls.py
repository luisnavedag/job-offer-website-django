from django.urls import path

from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'employer', views.EmployerDetail, basename='employer-detail')
urlpatterns = router.urls