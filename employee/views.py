from rest_framework import generics
from .models import Employee, Skill
from .serializers import EmployeeSerializer, SkillSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import Request
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAdminUser
from django.shortcuts import get_object_or_404
from API.permissions import IsEmployer, IsEmployee
from employer.models import Employer
from job_offers.models import JobOffer
from job_offers.serializers import JobOfferSerializer
from job_offers.filters import JobOfferFilter


class EmployeeCreate(APIView):
    """
    Creating a profile for an employee based on the logged-in user
    """
    def post(self, request: Request) -> Response:
        if Employer.objects.filter(user=request.user).exists():
            data = {'message': 'User already assigned as Employer'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        serializer = EmployeeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class EmployeeDetail(APIView):
    """
    Operations on the employee profile
    """
    def get(self, request: Request, pk: int) -> Response:
        employee = self.get_object(self)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request: Request, pk: int) -> Response:
        employee = self.get_object(self)

        serializer = EmployeeSerializer(employee, data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: Request, pk: int) -> Response:
        employee = self.get_object(self)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def get_object(self):
        obj = get_object_or_404(Employee, user=self.request.user.id)
        return obj


class SkillCreate(APIView):
    """
    Create a new skill
    """
    def post(self, request: Request) -> Response:
        serializer = SkillSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SkillDetail(APIView):
    """
    Operations for skills
    """
    permission_classes = [IsAdminUser]

    def get(self, request: Request, pk: int) -> Response:
        skill = self.get_object(pk)
        serializer = SkillSerializer(skill)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request: Request, pk: int) -> Response:
        skill = self.get_object(pk)

        serializer = SkillSerializer(skill, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: Request, pk: int) -> Response:
        skill = self.get_object(pk)
        skill.delete()
        return Response({'detail': 'Deleted.'}, status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def get_object(pk):
        obj = get_object_or_404(Skill, id=pk)
        return obj


class EmployeeListView(generics.ListAPIView):
    """
    Ordering, filtering, searching for employees
    """
    permission_classes = [IsEmployer]

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_fields = ('id', 'tags', 'status', 'city', 'skills__name')
    ordering_fields = ('user',)
    search_fields = ('city', 'tags')


class SkillListView(generics.ListAPIView):
    """
    Ordering, filtering, searching for skills
    """
    permission_classes = [IsAdminUser]

    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_fields = ('name',)
    ordering_fields = ('created',)
    search_fields = ('name',)


class EmployeeAplicationsListView(generics.ListAPIView):
    """
    Returns information about all applications of the logged in user
    """

    permission_classes = [IsEmployee]

    queryset = JobOffer.objects.all()
    serializer_class = JobOfferSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = JobOfferFilter
    ordering = ['-id']

    def get_queryset(self):
        """
        The function returns job offers for which the logged-in user has applied
        """
        return JobOffer.objects.filter(application__employee__user=self.request.user)
