from rest_framework.permissions import BasePermission

class IsDoctor(BasePermission):
    """
    Allows access only to users with the 'doctor' role.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'doctor'

class IsPharmacist(BasePermission):
    """
    Allows access only to users with the 'pharmacist' role.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'pharmacist'

class IsSecretary(BasePermission):
    """
    Allows access only to users with the 'secretary' role.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'secretary'

class IsClinicAdmin(BasePermission):
    """
    Allows access only to users who are admins of a clinic.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and hasattr(request.user, 'administered_clinics')

class IsOwnerOrAdmin(BasePermission):
    """
    Object-level permission to only allow owners of an object or admins to edit it.
    Assumes the model instance has a `user` or `doctor` attribute.
    """
    def has_object_permission(self, request, view, obj):
        # Admins can access everything
        if request.user.is_staff or (hasattr(request.user, 'administered_clinics') and obj.consultation.doctor.clinic in request.user.administered_clinics.all()):
             return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.consultation.doctor == request.user
