import secrets
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import SensitiveData
from .serializers import SensitiveDataSerializer, TokenRequestSerializer

class VaultViewSet(viewsets.GenericViewSet):
    """
    A secure vault for storing and retrieving encrypted data.
    """
    queryset = SensitiveData.objects.all()
    serializer_class = SensitiveDataSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Takes sensitive data, returns a token.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Generate a secure, URL-safe token
        token = secrets.token_urlsafe(32)

        serializer.save(token=token)

        return Response({'token': token}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], serializer_class=TokenRequestSerializer)
    def retrieve_data(self, request):
        """
        Takes a token, returns the sensitive data if the user is the intended recipient.
        """
        serializer = TokenRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['token']

        try:
            sensitive_data = SensitiveData.objects.get(token=token)
        except SensitiveData.DoesNotExist:
            return Response({'error': 'Invalid token'}, status=status.HTTP_404_NOT_FOUND)

        if sensitive_data.intended_recipient != request.user:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        return Response({'data': sensitive_data.data})
