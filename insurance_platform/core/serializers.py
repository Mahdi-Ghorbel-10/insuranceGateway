from rest_framework import serializers
from .models import User, Contract, Consultation, Clinic, FormTemplate

class FormTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormTemplate
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'role', 'specialty', 'clinic']

class ClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = '__all__'

class ConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultation
        fields = '__all__'

class ContractSerializer(serializers.ModelSerializer):
    diagnosis_data = serializers.CharField(write_only=True)
    prescription_data = serializers.CharField(write_only=True)
    insurer_user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Contract
        fields = [
            'id', 'consultation', 'insurer', 'claimed_by_pharmacy', 'status',
            'external_ref_id', 'created_at', 'updated_at',
            'diagnosis_token', 'prescription_token',
            'diagnosis_data', 'prescription_data', 'insurer_user_id'
        ]
        read_only_fields = ['status', 'created_at', 'updated_at', 'claimed_by_pharmacy', 'diagnosis_token', 'prescription_token']

class ContractUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ['status']
