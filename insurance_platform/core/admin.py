from django.contrib import admin
from .models import User, Clinic, Insurer, Pharmacy, Consultation, Contract, FulfilledItem

admin.site.register(User)
admin.site.register(Clinic)
admin.site.register(Insurer)
admin.site.register(Pharmacy)
admin.site.register(Consultation)
admin.site.register(Contract)
admin.site.register(FulfilledItem)
