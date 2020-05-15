"""Store media views"""

# Django REST Framework
from rest_framework import viewsets,mixins,status

# Django
from django.utils.translation import ugettext_lazy as _

# Permissions
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from myhandycrafts.stores.permissions import IsAdminorIsOwnerObject

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
                       viewsets.GenericViewSet):
    queryset = StoreMedia.objects.filter(active=True)
    permission_classes = [IsAdminorIsOwnerObject]
    serializer_class = StoreMediaModelSerializer

    def get_serializer_context(self):
        return {'user':self.request.user}


    def perform_destroy(self, instance):
        instance.active = False
        instance.deleted_at = timezone.now()
        instance.save()
        """add policies when object is deleted"""


