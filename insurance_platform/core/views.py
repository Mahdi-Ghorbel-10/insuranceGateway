from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from .models import User, Contract, Consultation, Insurer, Pharmacy, Clinic
from .serializers import UserSerializer, ContractSerializer, ConsultationSerializer, ContractUpdateSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

from .serializers import UserSerializer, ContractSerializer, ConsultationSerializer, ContractUpdateSerializer, ClinicSerializer, FormTemplateSerializer
from .models import FormTemplate

class FormTemplateViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing form templates.
    Only admins should be able to manage these.
    """
    queryset = FormTemplate.objects.all()
    serializer_class = FormTemplateSerializer
    permission_classes = [permissions.IsAdminUser]

class ClinicViewSet(viewsets.ModelViewSet):
    queryset = Clinic.objects.all()
    serializer_class = ClinicSerializer
    permission_classes = [permissions.IsAuthenticated] # Should be more specific, e.g., IsAdminUser

class InsurerViewSet(viewsets.ModelViewSet):
    queryset = Insurer.objects.all()
    serializer_class = UserSerializer # This should be an InsurerSerializer
    permission_classes = [permissions.IsAuthenticated]

class PharmacyViewSet(viewsets.ModelViewSet):
    queryset = Pharmacy.objects.all()
    serializer_class = UserSerializer # This should be a PharmacySerializer
    permission_classes = [permissions.IsAuthenticated]

from .permissions import IsDoctor, IsSecretary, IsOwnerOrAdmin

class ConsultationViewSet(viewsets.ModelViewSet):
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            self.permission_classes = [IsDoctor or IsSecretary]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsOwnerOrAdmin]
        else:
            self.permission_classes = [permissions.IsAuthenticated]
        return super(ConsultationViewSet, self).get_permissions()


    def get_queryset(self):
        """
        This view should return a list of all the consultations
        for the currently authenticated user's clinic.
        """
        user = self.request.user
        if user.role == 'doctor' or user.role == 'secretary':
            # Assuming users are linked to a clinic
            return Consultation.objects.filter(doctor__clinic=user.clinic)
        # Add other roles as needed
        return Consultation.objects.none()

    def perform_create(self, serializer):
        """
        A secretary can create a consultation, but it must be assigned to a doctor.
        A doctor creates a consultation for themselves.
        """
        if self.request.user.role == 'doctor':
            serializer.save(doctor=self.request.user)
        elif self.request.user.role == 'secretary':
            # The doctor should be specified in the request data
            serializer.save()

from .permissions import IsDoctor, IsPharmacist, IsOwnerOrAdmin

class ContractViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows contracts to be viewed or edited.
    """
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            self.permission_classes = [IsDoctor]
        elif self.action in ['fill', 'claim']:
            self.permission_classes = [IsPharmacist]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsOwnerOrAdmin]
        else:
            self.permission_classes = [permissions.IsAuthenticated]
        return super(ContractViewSet, self).get_permissions()

    def get_queryset(self):
        """
        This view should return a list of all the contracts
        for the currently authenticated user.
        """
        user = self.request.user
        if user.role == 'doctor':
            return Contract.objects.filter(consultation__doctor=user)
        elif user.role == 'pharmacist':
            # Pharmacists can see unclaimed contracts and contracts they have claimed
            return Contract.objects.filter(models.Q(claimed_by_pharmacy=None) | models.Q(claimed_by_pharmacy__user=user))
        elif user.role == 'insurer':
            return Contract.objects.filter(insurer__user=user) # Assuming Insurer has a user link
        elif user.is_staff:
            return Contract.objects.all()
        return Contract.objects.none()

    def perform_create(self, serializer):
        """
        Create a contract by first storing sensitive data in the vault
        and then saving the contract with the returned tokens.
        """
        diagnosis_data = self.request.data.get('diagnosis_data')
        prescription_data = self.request.data.get('prescription_data')
        insurer_user_id = self.request.data.get('insurer_user_id') # User ID of the insurer

        # In a real app, you would have a more robust way of getting the pharmacy user
        # For now, we assume any pharmacist can be the recipient for the prescription
        pharmacy_user = User.objects.filter(role='pharmacist').first()

        # 1. Store diagnosis in vault
        vault_response = self.store_in_vault(diagnosis_data, insurer_user_id)
        diagnosis_token = vault_response.get('token')

        # 2. Store prescription in vault
        vault_response = self.store_in_vault(prescription_data, pharmacy_user.id)
        prescription_token = vault_response.get('token')

from notifications.services import send_notification

        contract = serializer.save(
            diagnosis_token=diagnosis_token,
            prescription_token=prescription_token
        )

        # Send notification to patient
        patient_phone_number = self.request.data.get('patient_phone_number')
        if patient_phone_number:
            message = f"Your new insurance contract ID is: {contract.id}. Please present this at the pharmacy."
            send_notification(patient_phone_number, message)

    def store_in_vault(self, data, recipient_id):
        """
        A helper function to call the vault service.
        """
        # This is a simplified, direct call. In a real microservice architecture,
        # you would use something like requests or an RPC client.
        from vault.views import VaultViewSet

        vault_view = VaultViewSet()
        # Mocking a request object for the vault view
        class MockRequest:
            def __init__(self, user, data):
                self.user = user
                self.data = data

        # The user making the request to the vault is the current authenticated user
        user = self.request.user
        request_data = {'data': data, 'intended_recipient': recipient_id}
        mock_request = MockRequest(user, request_data)

        response = vault_view.create(mock_request)
        return response.data

    @action(detail=True, methods=['post'])
    def claim(self, request, pk=None):
        """
        Allows a pharmacist to claim a contract.
        """
        contract = self.get_object()
        user = request.user
        if user.role != 'pharmacist':
            return Response({'status': 'permission denied'}, status=status.HTTP_403_FORBIDDEN)
        if contract.claimed_by_pharmacy is not None:
            return Response({'status': 'contract already claimed'}, status=status.HTTP_400_BAD_REQUEST)

        # Assuming the pharmacist user is linked to a Pharmacy object
        pharmacy = Pharmacy.objects.get(user=user)
        contract.claimed_by_pharmacy = pharmacy
        contract.status = 'ready_for_pharmacy'
        contract.save()
        return Response({'status': 'contract claimed'})

    @action(detail=True, methods=['put'], serializer_class=ContractUpdateSerializer)
    def fill(self, request, pk=None):
        """
        Mark a contract as filled by a pharmacy.
        """
        contract = self.get_object()
        if request.user.role != 'pharmacist':
            return Response({'status': 'permission denied'}, status=status.HTTP_403_FORBIDDEN)

        # In a real implementation, you would decrypt and validate the invoice info
        contract.status = 'ready_to_submit'
        contract.save()
        return Response({'status': 'contract filled'})

    @action(detail=True, methods=['get'])
    def audit_certificate(self, request, pk=None):
        """
        Generate a PDF audit certificate for a contract.
        """
        from reportlab.pdfgen import canvas
        from django.http import HttpResponse

        contract = self.get_object()

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="contract_{contract.id}_audit.pdf"'

        p = canvas.Canvas(response)

        p.drawString(100, 800, f"Audit Certificate for Contract #{contract.id}")
        p.drawString(100, 780, f"Status: {contract.status}")
        p.drawString(100, 760, f"Created At: {contract.created_at.strftime('%Y-%m-%d %H:%M')}")

        if contract.consultation and contract.consultation.doctor:
            p.drawString(100, 740, f"Doctor: {contract.consultation.doctor.get_full_name()}")
            p.drawString(100, 720, f"Doctor's Signature: {contract.doctor_signature[:30]}...")

        if contract.claimed_by_pharmacy:
            p.drawString(100, 700, f"Pharmacy: {contract.claimed_by_pharmacy.name}")
            p.drawString(100, 680, f"Pharmacist's Signature: {contract.pharmacist_signature[:30]}...")

        # In a real app, you would add more details and a proper audit trail of state changes

        p.showPage()
        p.save()
        return response

    @action(detail=True, methods=['post'])
    def fulfill_partial(self, request, pk=None):
        """
        Partially fulfill a contract and create a follow-on contract for the remainder.
        """
        contract = self.get_object()
        if not contract.claimed_by_pharmacy or contract.claimed_by_pharmacy.user != request.user:
            return Response({'status': 'permission denied'}, status=status.HTTP_403_FORBIDDEN)

        fulfilled_items = request.data.get('fulfilled_items', []) # e.g., [{'item_description': 'Aspirin', 'quantity': 50}]

        for item in fulfilled_items:
            FulfilledItem.objects.create(
                contract=contract,
                item_description=item['item_description'],
                quantity_fulfilled=item['quantity_fulfilled']
            )

        contract.status = 'partially_filled'
        contract.save()

        # Create a new contract for the remaining items
        # This is a simplified example. In a real app, you would need to know
        # the original prescription to calculate the remaining items.
        new_contract = Contract.objects.create(
            consultation=contract.consultation,
            insurer=contract.insurer,
            parent_contract=contract,
            # The new contract needs a new prescription token for the remaining items
        )

        return Response({
            'status': 'partially fulfilled',
            'original_contract_id': contract.id,
            'follow_on_contract_id': new_contract.id
        })

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # In a real app, you'd return a proper token (e.g., JWT)
            return Response({"status": "success", "user": UserSerializer(user).data})
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)
