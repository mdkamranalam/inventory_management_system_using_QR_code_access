import io
import base64
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import qrcode
from .models import InventoryItem
from .serializers import InventoryItemSerializer

class InventoryItemViewSet(viewsets.ModelViewSet):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    # permission_classes = [IsAuthenticated]  # Uncomment for JWT auth

    @action(detail=True, methods=['get'])
    def generate_qr(self, request, pk=None):
        try:
            item = self.get_object()
            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            qr.add_data(item.qr_code_data)
            qr.make(fit=True)

            img = qr.make_image(fill='black', back_color='white')
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
            return Response({'qr_code': f'data:image/png;base64,{img_str}'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_queryset(self):
        queryset = InventoryItem.objects.all()
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(name__icontains=search_query) | \
                       queryset.filter(qr_code_data__icontains=search_query)
        return queryset