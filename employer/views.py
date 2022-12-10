from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import Request
from .serializers import EmployerSerializer
from .models import Employer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework import generics
from icecream import ic
from rest_framework import viewsets
from django.shortcuts import get_object_or_404


# class EmployerCreate(generics.CreateAPIView):
#     queryset = Employer.objects.all()
#     serializer_class = EmployerSerializer
#
#     def create(self, request, *args, **kwargs):
#         data = request.data | {"user": self.request.user.id}
#         serializer = self.get_serializer(data=data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#

# class EmployerDetail(APIView):
#     def get(self, request: Request, pk: int) -> Response:
#         if request.user.is_authenticated:
#             employer = Employer.objects.get(user=request.user)
#             serializer = EmployerSerializer(employer)
#             return Response(serializer.data, status=status.HTTP_200_OK)


class EmployerDetail(viewsets.ViewSet):
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer

    def create(self, request):
        data = request.data | {"user": self.request.user.id}
        serializer = self.serializer_class(data=data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        instance = self.get_object(self)
        serializer = self.serializer_class(instance)
        return Response(serializer.data)

    def update(self, request, pk=None):
        instance = self.get_object(self)
        data = request.data | {"user": request.user.id}
        serializer = self.serializer_class(instance, data=data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        instance = self.get_object(self)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def get_object(self):
        obj = get_object_or_404(Employer, user=self.request.user.id)
        return obj


