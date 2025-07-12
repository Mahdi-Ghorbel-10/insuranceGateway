from rest_framework import serializers
from .models import User, Contract, Consultation

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'role', 'specialty']

class ConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultation
        fields = '__all__'

class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = '__all__'
        read_only_fields = ['status', 'created_at', 'updated_at', 'claimed_by_pharmacy']

class ContractUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ['status']
