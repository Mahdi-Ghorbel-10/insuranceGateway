import uuid
from django.db import models
from django.conf import settings

class SensitiveData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # The encrypted data blob
    data = models.TextField()
    # The token that will be used to retrieve the data
    token = models.CharField(max_length=255, unique=True, db_index=True)
    # The user who can access this data (e.g., a specific pharmacist or insurer user)
    intended_recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='vault_data'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
