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

class ClinicViewSet(viewsets.ModelViewSet):
    queryset = Clinic.objects.all()
    serializer_class = UserSerializer # This should be a ClinicSerializer
    permission_classes = [permissions.IsAuthenticated]

class InsurerViewSet(viewsets.ModelViewSet):
    queryset = Insurer.objects.all()
    serializer_class = UserSerializer # This should be an InsurerSerializer
    permission_classes = [permissions.IsAuthenticated]

class PharmacyViewSet(viewsets.ModelViewSet):
    queryset = Pharmacy.objects.all()
    serializer_class = UserSerializer # This should be a PharmacySerializer
    permission_classes = [permissions.IsAuthenticated]

class ConsultationViewSet(viewsets.ModelViewSet):
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the consultations
        for the currently authenticated user.
        """
        user = self.request.user
        if user.role == 'doctor':
            return Consultation.objects.filter(doctor=user)
        # Add other roles as needed
        return Consultation.objects.none()

class ContractViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows contracts to be viewed or edited.
    """
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [permissions.IsAuthenticated]

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
        # Placeholder for creating a contract
        # The pharmacy is no longer chosen at creation
        serializer.save()

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
