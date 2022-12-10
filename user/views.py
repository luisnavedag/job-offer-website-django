from .models import User
from .serializers import RegisterSerializer, ChangePasswordSerializer
from rest_framework import generics, permissions
from rest_framework.views import APIView
from .email_service import SendEmailNewUser
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime


class RegisterView(APIView):
    """
    New user registration
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request) -> Response:
        serializer = RegisterSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        SendEmailNewUser(serializer.data).send_email()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserActivationView(APIView):
    """
    Activation via a link in the email for a new user
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request) -> Response:
        timestamp = float(request.query_params.get('timestamp'))
        timestamp_now = self._get_timestamp()

        if timestamp < timestamp_now:
            return Response({'message': f'Activation link has been expired'})

        user_id = request.query_params.get('id')
        user_to_activate = User.objects.filter(id=user_id).first()

        if user_to_activate:
            user_to_activate.is_active = True
            user_to_activate.save()
            return Response(RegisterSerializer(user_to_activate).data, status=status.HTTP_200_OK)

        return Response({'message': f'Account activation error'}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def _get_timestamp():
        return datetime.utcnow().timestamp()


class ChangePasswordView(generics.UpdateAPIView):
    """
    Changing the password for the logged-in user
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None) -> User:
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs) -> Response:
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        if not instance.check_password(serializer.data.get("old_password")):
            return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

        instance.set_password(serializer.data.get("new_password"))
        instance.save()
        response = {
            'status': 'success',
            'code': status.HTTP_200_OK,
            'message': 'Password updated successfully',
            'data': []
        }

        return Response(response)
