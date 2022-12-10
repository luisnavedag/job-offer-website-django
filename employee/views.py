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
from API.permissions import IsEmployer


class EmployeeCreate(APIView):
    def post(self, request: Request) -> Response:
        data = {
            "user": self.request.user.id,
            "tags": request.data.get('tags', None),
            "city": request.data.get('city', None),
            "linkdin": request.data.get('linkdin', None),
            "status": request.data.get('status', None),
            "about_yourself": request.data.get('about_yourself', None),
        }

        skills = request.data.get('skills', None)
        if skills:
            data['skills'] = skills

        serializer = EmployeeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeDetail(APIView):
    def get(self, request: Request, pk: int) -> Response:
        employee = self.get_object(self)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request: Request, pk: int) -> Response:
        employee = self.get_object(self)

        serializer = EmployeeSerializer(employee, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, pk: int) -> Response:
        employee = self.get_object(self)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def get_object(self):
        obj = get_object_or_404(Employee, user=self.request.user.id)
        return obj


class SkillCreate(APIView):
    def post(self, request: Request) -> Response:
        serializer = SkillSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SkillDetail(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request: Request, pk: int) -> Response:
        skill = self.get_object(pk)
        serializer = SkillSerializer(skill)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request: Request, pk: int) -> Response:
        skill = self.get_object(pk)

        serializer = SkillSerializer(skill, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, pk: int) -> Response:
        skill = self.get_object(pk)
        skill.delete()
        return Response({'detail': 'Deleted.'}, status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def get_skill(pk: int) -> Skill:
        return Skill.objects.get(pk=pk)

    @staticmethod
    def get_object(pk):
        obj = get_object_or_404(Skill, id=pk)
        return obj


class EmployeeListView(generics.ListAPIView):
    permission_classes = [IsEmployer]

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_fields = ('tags', 'status', 'city', 'skills__name')
    ordering_fields = ('user',)
    search_fields = ('city', 'tags')


class SkillListView(generics.ListAPIView):
    permission_classes = [IsAdminUser]

    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_fields = ('name',)
    ordering_fields = ('created',)
    search_fields = ('name',)
