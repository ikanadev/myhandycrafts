"""Participant Serializer."""


# Django REST Framework
from rest_framework import serializers

#Django
from django.utils.translation import ugettext_lazy as _

# models
from myhandycrafts.fairs.models import Participant
from myhandycrafts.users.models import User

# serializer
from myhandycrafts.users.serializers import UserShortDetailSerializer
from myhandycrafts.fairs.serializers import FairShortDetailModelSerializer

# utils
from django.utils import timezone


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
                                      active=True).exists():
            raise serializers.ValidationError(_("Already exists User on fair"))

        return super(ParticipantModelSerializer,self).create(data)
    #
    # def update(self, instance, data):
    #     if Participant.objects.filter(user=data['user'],
    #                                   fair=data['fair'],
    #                                   active=True).exclude(pk=instance.pk).exists():
    #         raise serializers.ValidationError(_("Already exists User on fair"))
    #
    #     return super(ParticipantModelSerializer,self).update(instance,data)


class ParticipantDetailModelSerializer(serializers.ModelSerializer):
    """Participant model serializer."""
    user = UserShortDetailSerializer(many=False)
    admin = UserShortDetailSerializer(many=False)
    fair = FairShortDetailModelSerializer(many=False)

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



class AddParticipantSerializer(serializers.Serializer):
    """Add  participant serializer.
    
    Handle the addition of a new participant to fair.
    Fair object must be provide in the context"""


    user = serializers.IntegerField()
    user_description = serializers.CharField(max_length=2048,required=False)
    admin_description = serializers.CharField(max_length=2048,required=False)
    state = serializers.CharField(max_length=2)


    def validate_user(self,data):
        """Verify user isn't already member."""
        try:
            user = User.objects.get(pk=data,active=True,is_staff=False)
        except User.DoesNotExist:
            raise serializers.ValidationError(_('User not valid'))

        fair = self.context['fair']
        q = Participant.objects.filter(fair=fair,
                                       user=user,
                                       active=True)
        if q.exists():
            raise serializers.ValidationError(_('User is already participate of this fair'))
        self.context['user']=user
        return data

    def create(self,data):
        """Create a new participant"""
        admin_user=self.context['request_user']
        user=self.context['user']
        fair = self.context['fair']
        data.pop('user')

        participant = Participant.objects.create(
            **data,
            user=user,
            admin=admin_user,
            fair=fair,
            created_by=admin_user.pk
        )
        return participant


class UpdateAdminParticipantSerializer(serializers.Serializer):
    """Add  participant serializer.

    Handle the addition of a new participant to fair.
    Fair object must be provide in the context"""

    admin_description = serializers.CharField(max_length=2048, required=False)
    state = serializers.CharField(max_length=2,required=True)

    def update(self, instance, data):
        admin_user = self.context['request_user']
        instance.admin = admin_user
        instance.admin_description = data['admin_description']
        instance.state = data['state']
        instance.updated_by = admin_user.pk
        instance.save()
        return instance


class JoinParticipantSerializer(serializers.Serializer):
    """Join participant serializer.

    Handle the addition of a new participant to fair.
    Fair object must be provide in the context"""
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    user_description = serializers.CharField(max_length=2048, required=False)

    def validate(self, attrs):
        user = self.context['request_user']
        fair = self.context['fair']
        if user.is_staff:
            raise serializers.ValidationError(_("Admin can't join to fair"))
        q = Participant.objects.filter(fair=fair,
                                       user=user,
                                       active=True)
        if q.exists():
            raise serializers.ValidationError(_("User is already participate of this fair"))
        return attrs

    def create(self, data):
        """Create a new participant"""
        user = self.context['request_user']
        fair = self.context['fair']
        participant = Participant.objects.create(
            **data,
            user=user,
            fair=fair,
            created_by=user.pk,
            state='PP'
        )
        return participant


class UpdateParticipantSerializer(serializers.Serializer):
    """update participant user_description serializer.

    Handle the addition of a new participant to fair.
    Fair object must be provide in the context"""
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    user_description = serializers.CharField(max_length=2048, required=False)

    def update(self, instance, data):
        user = self.context['request_user']
        instance.user_description = data['user_description']
        instance.updated_by = user.pk
        instance.save()
        return instance


class DeclineParticipantSerializer(serializers.Serializer):
    """decline participant user_description serializer.

    Handle the decline join request to fair.
    Fair object must be provide in the context"""

    def update(self, instance, data):
        now = timezone.now().date()
        if instance.fair.date_init >= now:
            raise serializers.ValidationError('Ongoing fair cannot be modified.')
        user = self.context['request_user']
        instance.state = 'DD'
        instance.updated_by = user.pk
        instance.save()
        return instance

class RejoinParticipantSerializer(serializers.Serializer):
    """decline participant user_description serializer.

    Handle the re join request to fair.
    Fair object must be provide in the context"""

    def update(self, instance, data):
        now = timezone.now().date()
        if instance.fair.date_init >= now:
            raise serializers.ValidationError('Ongoing fair cannot be modified.')
        user = self.context['request_user']
        instance.state = 'PP'
        instance.updated_by = user.pk
        instance.save()
        return instance