"""Fair media views"""

# Django REST Framework
from rest_framework import viewsets,mixins,status
# Django
from django.utils.translation import ugettext_lazy as _

# Permissions
from rest_framework.permissions import IsAuthenticated,IsAdminUser

# models
from myhandycrafts.fairs.models import FairMedia

# Serializer
from myhandycrafts.fairs.serializers import FairMediaModelSerializer

# Django Util
from django.utils import timezone
from rest_framework.filters import SearchFilter, OrderingFilter

from rest_framework.response import Response


class FairMediaViewSet(mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       # mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    queryset = FairMedia.objects.filter(active=True)
    permission_classes = [IsAuthenticated,IsAdminUser]
    serializer_class = FairMediaModelSerializer
    # # filter_backends = (OrderingFilter)
    # ordering_fields = ('order',)
    # ordering = ('order',)


    def perform_destroy(self, instance):
        instance.active = False
        instance.deleted_at = timezone.now()
        instance.save()
        """add policies when object is deleted"""

