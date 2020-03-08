"""Profile serializer."""

# Django
from rest_framework import serializers

# Model
from myhandycrafts.users.models import Profile

class ProfileModelSerializer(serializers.ModelSerializer):
    """Profile Model serializer."""

    class Meta:
        model=Profile
        fields=(
            'picture',
            'biography',
            'ci',
            'birth_date',
            'address',
            'category',
            'nit',
            'nit_bussiness_name',
            'nit_is_active',
            'phone_number',
            'website',
            'has_wattsapp',
            'has_facebook',
            'addres_facebook',
            'reputation',
            'publications',
            'requests',
            'stores',
            'participation_in_fairs',
        )

        read_only_field=(
            'reputation',
            'publications',
            'requests',
            'stores',
            'participation_in_fairs',
        )