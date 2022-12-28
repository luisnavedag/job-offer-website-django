from rest_framework import generics
from API.permissions import IsEmployer, IsJobOfferCreator
from .models import JobOffer
from .serializers import JobOfferSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime
from django.shortcuts import get_object_or_404
from rest_framework import status


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
