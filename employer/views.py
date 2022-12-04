from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import Request
from .serializers import EmployerSerializer
from .models import Employer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter


class EmployerCreate(APIView):
    def post(self, request: Request) -> Response:
        data = {
            "user": self.request.user.id,
            "company_name": request.data.get('company_name', None),
            "company_size": request.data.get('company_size', None),
            "website": request.data.get('website', None),
        }

        serializer = EmployerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployerDetail(APIView):
    def get(self, request: Request, pk: int) -> Response:
        if request.user.is_authenticated:
            employer = Employer.objects.get(user=request.user)
            serializer = EmployerSerializer(employer)
            return Response(serializer.data, status=status.HTTP_200_OK)
