from django.urls import path

from . import views

from rest_framework.routers import DefaultRouter

# urlpatterns = [
#     path('employer/', views.EmployerCreate.as_view(), name='employer-create'),
#     # path('employer/<int:pk>/', views.EmployerDetail.as_view(), name='employer-detail'),
#     # path('employees/', views.EmployeeListView.as_view(), name='employees'),
# ]


router = DefaultRouter()
router.register(r'employer', views.EmployerDetail, basename='employer-detail')
urlpatterns = router.urls