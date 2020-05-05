"""Store media views"""

# Django REST Framework
from rest_framework import viewsets,mixins,status

# Django
from django.utils.translation import ugettext_lazy as _

# Permissions
from rest_framework.permissions import IsAuthenticated,IsAdminUser

# models
from myhandycrafts.stores.models import StoreMedia

# Serializer
from myhandycrafts.stores.serializers import StoreMediaModelSerializer

# Django Util
from django.utils import timezone
from rest_framework.filters import SearchFilter, OrderingFilter

from rest_framework.response import Response


class StoreMediaViewSet(mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       # mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    queryset = StoreMedia.objects.filter(is_deleted=False)
    permission_classes = [IsAuthenticated]
    serializer_class = StoreMediaModelSerializer
    # # filter_backends = (OrderingFilter)
    # ordering_fields = ('order',)
    # ordering = ('order',)


    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.deleted_at = timezone.now()
        instance.save()
        """add policies when object is deleted"""

