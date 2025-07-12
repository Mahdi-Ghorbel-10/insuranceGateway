from django.contrib.auth.models import AbstractUser
from django.db import models

class Clinic(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class User(AbstractUser):
    ROLE_CHOICES = (
        ('doctor', 'Doctor'),
        ('secretary', 'Secretary'),
        ('pharmacist', 'Pharmacist'),
        ('insurer', 'Insurer'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    specialty = models.CharField(max_length=100, blank=True, null=True)
    license_number = models.CharField(max_length=100, blank=True, null=True)
    clinic = models.ForeignKey(Clinic, on_delete=models.SET_NULL, related_name='staff', null=True, blank=True)

    def __str__(self):
        return self.name

class Insurer(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Pharmacy(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class FormTemplate(models.Model):
    name = models.CharField(max_length=255)
    specialty = models.CharField(max_length=100, unique=True)
    template_schema = models.JSONField() # Defines the form fields

    def __str__(self):
        return f"{self.name} ({self.specialty})"

class Consultation(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='consultations')
    patient_insurance_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class Contract(models.Model):
    diagnosis_token = models.CharField(max_length=255, null=True, blank=True)
    prescription_token = models.CharField(max_length=255, null=True, blank=True)
    form_data = models.JSONField(null=True, blank=True) # For specialty-specific form data
    parent_contract = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='follow_on_contracts')
    doctor_signature = models.TextField(blank=True, null=True)
    pharmacist_signature = models.TextField(blank=True, null=True)
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('ready_for_pharmacy', 'Ready for Pharmacy'),
        ('partially_filled', 'Partially Filled'),
        ('ready_to_submit', 'Ready to Submit'),
        ('submitted', 'Submitted'),
        ('submitted_doctor_only', 'Submitted (Doctor Only)'),
        ('submitted_pharmacy_only', 'Submitted (Pharmacy Only)'),
        ('archived', 'Archived'),
        ('expired', 'Expired'),
    )
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name='contracts', null=True, blank=True)
    insurer = models.ForeignKey(Insurer, on_delete=models.CASCADE, related_name='contracts')
    claimed_by_pharmacy = models.ForeignKey(Pharmacy, on_delete=models.SET_NULL, related_name='claimed_contracts', null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='draft')
    external_ref_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class FulfilledItem(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='fulfilled_items')
    item_description = models.CharField(max_length=255) # e.g., "Aspirin 100mg"
    quantity_fulfilled = models.PositiveIntegerField()
    fulfilled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item_description} for contract {self.contract.id}"
