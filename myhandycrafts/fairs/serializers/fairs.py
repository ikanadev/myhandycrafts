""""Fair serialisers."""

# Django REST Framework
from rest_framework import serializers

# models
from myhandycrafts.fairs.models import Fair


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
            'ubicacion',
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



class FairCreateUpdateSeralizer(serializers.Serializer):
    """Fair Create Serializer.
    Only admin can create, update, and delete fair
    """

    # user = serializers.
    # municipality = serializers.
    # name = serializers.
    # description = serializers.
    # ubicacion = serializers.
    # gps = serializers.
    # date_init = serializers.
    # date_end = serializers.
    # time_init = serializers.
    # time_end = serializers.
    # is_limited = serializers.
    # participant_limit = serializers.
    # reputation = serializers.
    # publications = serializers.
    # visits = serializers.

    class Meta:
        model = Fair
        fields = (
            'id',
            'user',
            'municipality',
            'name',
            'description',
            'ubicacion',
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