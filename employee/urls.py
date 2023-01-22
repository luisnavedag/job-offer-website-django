from django.urls import path

from . import views

urlpatterns = [
    path('employee/', views.EmployeeCreate.as_view(), name='employee-create'),
    path('employee/<str:pk>/', views.EmployeeDetail.as_view(), name='employee-detail'),
    path('employee/applications/', views.EmployeeAplicationsListView.as_view(), name='employee-applications'),
    path('employees/', views.EmployeeListView.as_view(), name='employees'),

    path('skill/', views.SkillCreate.as_view(), name='skill-create'),
    path('skill/<int:pk>/', views.SkillDetail.as_view(), name='skill-detail'),
    path('skills/', views.SkillListView.as_view(), name='skills'),
]
