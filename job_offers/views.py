from rest_framework import status, generics
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from API.permissions import IsEmployer, IsJobOfferCreator
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from employer.models import Subscription
from .models import JobOffer
from .serializers import JobOfferSerializer
from .filters import JobOfferFilter
from datetime import datetime


class JobOfferDetail(generics.UpdateAPIView):
    """
    Update of the job offer by the owner of the offer
    """
    queryset = JobOffer.objects.all()
    serializer_class = JobOfferSerializer
    permission_classes = [IsEmployer, IsJobOfferCreator]


class JobOfferVerification(APIView):
    """
    Approval by the admin of the job offer entered by employers
    """
    permission_classes = [IsAdminUser]

    def get(self, request, pk) -> Response:
        timestamp = float(request.query_params.get('expiration_timestamp', 0))
        timestamp_now = self._get_timestamp()

        if timestamp < timestamp_now:
            return Response({'message': f'Activation link has been expired'})

        title = request.query_params.get('title', None)

        job_offer = get_object_or_404(JobOffer, id=pk, title=title)

        job_offer.verified = True
        job_offer.save()
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
    serializer_class = JobOfferSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = JobOfferFilter

    def get_queryset(self):
        """
        The function returns offers that have valid subscriptions
        """
        subscriptions = Subscription.get_valid_subscriptions()
        return JobOffer.objects.filter(id__in=[subscription.job_offer.id for subscription in subscriptions])

    def list(self, request, *args, **kwargs):
        """
        Offers will be sorted based on bids before sending the request
        """
        response = super().list(request, *args, **kwargs)
        response.data = sorted(response.data, key=lambda x: x['days_to_raise'])
        return response
