""""Fair serialisers."""

# Django REST Framework
from rest_framework import serializers

# models
from myhandycrafts.fairs.models import Fair

#serializer
from myhandycrafts.users.serializers import UserShortDetailSerializer
from myhandycrafts.maps.serializers import MunicipalityListSerializer
from myhandycrafts.fairs.serializers.fairmedias import FairMediaModelSerializer

class FairModelSerializer(serializers.ModelSerializer):
    """Fair Model Serializer."""
    class Meta:
        model = Fair
        fields = (
            'id',
            'user',
            'municipality',
            'name',
            'description',
            'location',
            'gps',
            'date_init',
            'date_end',
            'time_init',
            'time_end',
            'is_limited',
            'participant_limit',
            'reputation',
            'publications',
            'visits',
        )

    def validate_user(self,data):
        return self.context['user']


class FairDetailModelSerializer(serializers.ModelSerializer):
    """Fair Model Serializer."""

    user = UserShortDetailSerializer(many=False)
    municipality = MunicipalityListSerializer(many=False)
    class Meta:
        model = Fair
        fields = (
            'id',
            'user',
            'municipality',
            'name',
            'description',
            'location',
            'gps',
            'date_init',
            'date_end',
            'time_init',
            'time_end',
            'is_limited',
            'participant_limit',
            'reputation',
            'publications',
            'visits',
        )


class FairCreateUpdateSerializer(serializers.Serializer):
    """Fair Create Serializer.
    Only admin can create, update, and delete fair
    """
    class Meta:
        model = Fair
        fields = (
            'id',
            'user',
            'municipality',
            'name',
            'description',
            'location',
            'gps',
            'date_init',
            'date_end',
            'time_init',
            'time_end',
            'is_limited',
            'participant_limit',
            'reputation',
            'publications',
            'visits',
        )


class FairFeedModelSerializer(serializers.ModelSerializer):
    """Fair Model Serializer."""

    user = UserShortDetailSerializer(many=False)
    municipality = MunicipalityListSerializer(many=False)
    fairmedias = FairMediaModelSerializer(many=True)


    class Meta:
        model = Fair
        fields = (
            'id',
            'user',
            'municipality',
            'name',
            'description',
            'location',
            'gps',
            'date_init',
            'date_end',
            'time_init',
            'time_end',
            'is_limited',
            'participant_limit',
            'reputation',
            'publications',
            'visits',
            'fairmedias',
        )


class FairShortDetailModelSerializer(serializers.ModelSerializer):
    """Fair Model Serializer."""
    class Meta:
        model = Fair
        fields = (
            'id',
            'name',
            'description',
        )