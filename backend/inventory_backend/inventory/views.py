import io
import base64
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
import qrcode
from .models import InventoryItem
from .serializers import InventoryItemSerializer

class InventoryItemViewSet(viewsets.ModelViewSet):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer

    # Custom endpoint to generate QR code for an item
    @action(detail=True, methods=['get'])
    def generate_qr(self, request, pk=None):
        item = self.get_object()
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(item.qr_code_data)  # QR code contains the qr_code_data field
        qr.make(fit=True)

        # Generate QR code image
        img = qr.make_image(fill='black', back_color='white')
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        # Convert to base64 to send to frontend without saving to disk
        img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return Response({'qr_code': f'data:image/png;base64,{img_str}'})

    # Custom search endpoint
    def get_queryset(self):
        queryset = InventoryItem.objects.all()
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(name__icontains=search_query) | \
                       queryset.filter(qr_code_data__icontains=search_query)
        return queryset