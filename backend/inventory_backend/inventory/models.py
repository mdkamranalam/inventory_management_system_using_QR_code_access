from django.db import models

class InventoryItem(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    qr_code_data = models.CharField(max_length=255, unique=True, blank=True)  # e.g., "item-<id>"
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.qr_code_data:
            self.qr_code_data = f"item-{self.id or InventoryItem.objects.count() + 1}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name