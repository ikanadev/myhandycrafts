"""Store serializer."""

# Django REST Framework
from rest_framework import serializers

# Models
from myhandycrafts.stores.models import Store


class StoreModelSerializer(serializers.ModelSerializer):
    """Store model serializer"""

    class Meta:
        model = Store
        fields = (
            'id',
            'user',
            'municipality',
            'name',
            'description',
            'ubicacion',
            'gps',
            'reputation',
            'publications',
            'visits',
        )

        read_only_fields = (
            'reputation',
            'publications',
            'visits',
        )

    def validate_user(self,data):
        user = self.context['user']
        if not user.is_staff:
            if user !=data:
                raise serializers.ValidationError('You dont have permision for this action')
        return data

