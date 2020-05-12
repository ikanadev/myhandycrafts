"""Store serializer."""

# Django REST Framework
from rest_framework import serializers

# Models
from myhandycrafts.stores.models import Store

# Django
from django.utils.translation import ugettext_lazy as _

# Serializers
from myhandycrafts.users.serializers import UserShortDetailSerializer
from myhandycrafts.maps.serializers import MunicipalityListSerializer



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
                'location',
                'gps',
                'reputation',
                'publications',
                'visits',
                'created_at',
                'updated_at',
        )
        read_only_fields = (
            'reputation',
            'publications',
            'visits',
            'created_at',
            'updated_at',
        )

    # def validate_user(self,data):
    #     user = self.context['user']
    #     if not user.is_staff:
    #         if user !=data:
    #             raise serializers.ValidationError('You dont have permision for this action')
    #     return data


    def validate(self,data):
        user = self.context['user']
        if not user.is_staff:
            if user != data['user']:
                raise serializers.ValidationError('You dont have permision for this action')
        return data

    def update(self, instance, data):
        user = self.context['user']
        if not user.is_staff:
            if user != instance.user:
             raise serializers.ValidationError(_("You dont have permision for this action"))

        return super(StoreModelSerializer, self).update(instance, data)


class StoreDetailSerializer(serializers.ModelSerializer):
    user = UserShortDetailSerializer(many=False)
    municipality = MunicipalityListSerializer(many=False)

    class Meta:
        model = Store
        fields = (
                'id',
                'user',
                'municipality',
                'name',
                'description',
                'location',
                'gps',
                'reputation',
                'publications',
                'visits',
                'created_at',
                'updated_at',
        )