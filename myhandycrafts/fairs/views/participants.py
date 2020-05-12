"""Participants ViewSet."""

# Django REST Framework
from rest_framework import mixins,viewsets
from rest_framework.filters import SearchFilter,OrderingFilter
#permission
from rest_framework.permissions import  IsAuthenticated,IsAdminUser

# Models
from myhandycrafts.fairs.models import Participant

# Serializer
from myhandycrafts.fairs.serializers import ParticipantModelSerializer

# TIME
from django.utils import timezone


class ParticipantViewSet(viewsets.ModelViewSet):
    """Participant  view set
    handle admin CRUD
    """
    queryset = Participant.objects.filter(active=True)
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = ParticipantModelSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('user',)
    ordering_fields = ('user', 'created_at',)
    ordering = ('user','created_at')

    def perform_destroy(self, instance):
        instance.active=False
        instance.deleted_at = timezone.now()
        instance.save()
        """add policies when object is deleted"""
