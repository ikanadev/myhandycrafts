"""Post media views"""

# Django REST Framework
from rest_framework import viewsets,mixins,status

# Django
from django.utils.translation import ugettext_lazy as _

# Permissions
from rest_framework.permissions import IsAuthenticated,IsAdminUser

# models
from myhandycrafts.posts.models import PostMedia

# Serializer
from myhandycrafts.posts.serializers import PostMediaModelSerializer

# Django Util
from django.utils import timezone
from rest_framework.filters import SearchFilter, OrderingFilter

from rest_framework.response import Response


class PostMediaViewSet(mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       # mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    queryset = PostMedia.objects.filter(active=True)
    permission_classes = [IsAuthenticated]
    serializer_class = PostMediaModelSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ()
    ordering_fields = ('order',
                       )
    ordering = ('order')


    def perform_destroy(self, instance):
        instance.active=False
        instance.deleted_at = timezone.now()
        instance.save()
        """add policies when object is deleted"""

