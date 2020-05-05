"""Fair views"""

# Djnago REST Framework
from rest_framework import viewsets

# Permissions
from rest_framework.permissions import IsAuthenticated,IsAdminUser

# models
from myhandycrafts.fairs.models import Fair

# Serializer
from myhandycrafts.fairs.serializers import FairModelSerializer

# Django Util
from django.utils import timezone
from rest_framework.filters import SearchFilter, OrderingFilter



class FairViewSet(viewsets.ModelViewSet):

    queryset = Fair.objects.filter(is_deleted=False)
    permission_classes = [IsAuthenticated,IsAdminUser]
    serializer_class = FairModelSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('name','created_at','date_init',)
    ordering = ('name',)


    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.deleted_at = timezone.now()
        instance.save()
        """add policies when object is deleted"""


