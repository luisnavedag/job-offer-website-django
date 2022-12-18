from rest_framework import status
from rest_framework.response import Response
from .serializers import EmployerSerializer, SubscriptionSerializer
from .models import Employer, Subscription
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from employee.models import Employee
from rest_framework import generics
from API.permissions import IsEmployer
from rest_framework.views import APIView
from rest_framework.request import Request
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter


class EmployerDetail(viewsets.GenericViewSet):
    """
    Performing an operation for an employer
    """
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer

    def create(self, request) -> Response:
        if Employee.objects.filter(user=request.user).exists():
            data = {'message': 'User already assigned as Employee'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None) -> Response:
        instance = self.get_object()
        serializer = self.serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None) -> Response:
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None) -> Response:
        instance = self.get_object()
        instance.delete()
        data = {'message': 'Employer has been removed'}
        return Response(data, status=status.HTTP_204_NO_CONTENT)

    def get_object(self):
        obj = get_object_or_404(Employer, user=self.request.user.id)
        return obj


class SubscriptionCreate(APIView):
    """
    Creating a subscription for a logged-in employer
    """
    permission_classes = [IsEmployer]

    def post(self, request: Request) -> Response:
        serializer = SubscriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SubscriptionList(generics.ListAPIView):
    """
    Return subscription list. Ability to add appropriate filters
    """
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsEmployer]

    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ('type',)
    ordering_fields = ('created', 'type', 'first_day', 'last_day')
    ordering = ['last_day']

    def get_queryset(self):
        queryset = Subscription.objects.filter(employer__user=self.request.user)
        return queryset
