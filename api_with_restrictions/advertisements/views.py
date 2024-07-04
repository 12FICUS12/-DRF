from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from filters import AdvertisementFilter
from models import Advertisement
from permissions import IsOwnerOrReadOnly
from serializers import AdvertisementSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['status', 'created_at', 'status']



    def get_permissions(self):
        """Получение прав для действий."""
        if self.action == "create":
            return [IsAuthenticated()]

        elif self.action in ["create", "update", "partial_update"]:
            return [IsOwnerOrReadOnly()]
        return []
    def get_queryset(self):
        """Получение списка объявлений."""
        list = Advertisement.objects.all()
        queryset = AdvertisementFilter(data=self.request.GET, queryset=list, request=self.request).qs
        serializer = AdvertisementSerializer(queryset, many=True)
        return Response(serializer.data)
