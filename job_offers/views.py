from rest_framework import status, generics
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import Request
from general_utils.permissions import IsJobOfferCreator, IsEmployee
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction
from employer.models import Subscription
from employee.models import Employee
from .models import JobOffer, Application
from .serializers import JobOfferSerializer, JobOfferFilterSerializer
from .filters import JobOfferFilter
from .tasks import send_matchmaking_email
from job_offers.email_service.email_service import SendEmailJobOfferNewApplication
from job_offers.email_service.job_offer_new_application_form import job_offer_new_application_email_form
from datetime import datetime


class JobOfferDetail(generics.UpdateAPIView):
    """
    Update of the job offer by the owner of the offer
    """
    queryset = JobOffer.objects.all()
    serializer_class = JobOfferSerializer
    permission_classes = [IsJobOfferCreator]


class JobOfferVerification(APIView):
    """
    Approval by the admin of the job offer entered by employers
    If a user with the required skills is found, an email with an offer will be sent to him
    """
    permission_classes = [IsAdminUser]

    @transaction.atomic
    def get(self, request: Request, pk) -> Response:
        timestamp = float(request.query_params.get('expiration_timestamp', 0))
        timestamp_now = self._get_timestamp()

        if timestamp < timestamp_now:
            return Response({'message': f'Activation link has been expired'})

        title = request.query_params.get('title', None)

        job_offer = get_object_or_404(JobOffer, id=pk, title=title)

        job_offer.verified = True
        job_offer.save()

        data = {
            'job_offer_id': pk,
        }

        send_matchmaking_email.delay(data)

        message = {'message': f'The job offer titled - {title} - has been verified'}
        return Response(message, status=status.HTTP_200_OK)

    @staticmethod
    def _get_timestamp():
        return datetime.utcnow().timestamp()


class JobOfferListView(generics.ListAPIView):
    """
    List of available job offers. Offers can be filtered accordingly
    """
    permission_classes = [AllowAny]

    queryset = JobOffer.objects.all()
    serializer_class = JobOfferFilterSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = JobOfferFilter

    def get_queryset(self) -> JobOffer:
        """
        The function returns offers that have valid subscriptions
        """
        subscriptions = Subscription.get_valid_subscriptions()
        return JobOffer.objects.filter(
            id__in=[subscription.job_offer.id for subscription in subscriptions],
            verified=True
        )

    def list(self, request, *args, **kwargs) -> Response:
        """
        Offers will be sorted based on bids before sending the request
        """
        response = super().list(request, *args, **kwargs)
        response.data = sorted(response.data, key=lambda x: x['days_to_raise'])
        return response


class JobOfferApplication(APIView):
    """
    The application of a logged-in employee for a given position
    """
    permission_classes = [IsEmployee]

    def get(self, request: Request, pk: int) -> Response:
        job_offer_instance = get_object_or_404(JobOffer, id=pk)
        employee_instance = Employee.objects.get(user=request.user)

        if Application.objects.filter(job_offer=job_offer_instance, employee=employee_instance).exists():
            response = {'message': 'The application for this position has already been submitted'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        Application.objects.create(
            job_offer=job_offer_instance,
            employee=employee_instance
        )

        data = {
            'employee_id': employee_instance.id,
            'job_offer_id': job_offer_instance.id,
            'job_offer_title': job_offer_instance.title
            }

        send_email_instance = SendEmailJobOfferNewApplication(job_offer_new_application_email_form)
        send_email_instance.email_data = data
        send_email_instance.send_email()

        response = {'message': 'Application for the position have been submitted'}

        return Response(response, status=status.HTTP_200_OK)
