from rest_framework import serializers
from .models import SensitiveData

class SensitiveDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensitiveData
        fields = ['id', 'data', 'token', 'intended_recipient']
        read_only_fields = ['id', 'token', 'created_at']

class TokenRequestSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255)
