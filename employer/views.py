from rest_framework import status
from rest_framework.response import Response
from .serializers import EmployerSerializer
from .models import Employer
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from employee.models import Employee


class EmployerDetail(viewsets.GenericViewSet):
    """
    Performing an operation for an employer
    """
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer

    def create(self, request):
        if Employee.objects.filter(user=request.user).exists():
            data = {'message': 'User already assigned as Employee'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        instance = self.get_object()
        serializer = self.serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        instance = self.get_object()
        instance.delete()
        data = {'message': 'Employer has been removed'}
        return Response(data, status=status.HTTP_204_NO_CONTENT)

    def get_object(self):
        obj = get_object_or_404(Employer, user=self.request.user.id)
        return obj
