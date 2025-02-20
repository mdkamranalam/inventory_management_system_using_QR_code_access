from django.db import models

class InventoryItem(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    qr_code_data = models.CharField(max_length=255, unique=True)  # Stores QR code content (e.g., an ID or URL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name