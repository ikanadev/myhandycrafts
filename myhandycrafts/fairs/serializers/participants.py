"""Participant Serializer."""


# Django REST Framework
from rest_framework import serializers

#Django
from django.utils.translation import ugettext_lazy as _

# models
from myhandycrafts.fairs.models import Participant



class ParticipantModelSerializer(serializers.ModelSerializer):
    """Participant model serializer."""

    class Meta:
        model = Participant
        fields = (
            'id',
            'user',
            'admin',
            'fair',
            'user_description',
            'admin_description',
            'state',
        )

    def validate(self, data):
        return data

    def create(self, data):
        if Participant.objects.filter(user=data['user'],
                                      fair=data['fair'],
                                      is_deleted=False).exists():
            raise serializers.ValidationError(_("Already exists User on fair"))

        return super(ParticipantModelSerializer,self).create(data)

    def update(self, instance, data):
        if Participant.objects.filter(user=data['user'],
                                      fair=data['fair'],
                                      is_deleted=False).exclude(pk=instance.pk).exists():
            raise serializers.ValidationError(_("Already exists User on fair"))

        return super(ParticipantModelSerializer,self).update(instance,data)





