from django.urls import path

from . import views

urlpatterns = [

    path('job-offer/<int:pk>/', views.JobOfferDetail.as_view(), name='job-offer-detail'),
    path('job-offer/varification/<int:pk>/', views.JobOfferVerification.as_view(), name='job_offer_verification'),
    path('job-offers/', views.JobOfferListView.as_view(), name='job-offers'),

]
