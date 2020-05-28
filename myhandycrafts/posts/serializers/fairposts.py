""""FairPost serialisers."""
#django
from django.utils.translation import ugettext_lazy as _

# Django REST Framework
from rest_framework import serializers

# models
from myhandycrafts.posts.models import FairPost
from myhandycrafts.fairs.models import Participant

# serializer
from myhandycrafts.posts.serializers import PostDetailModelSerializer
from myhandycrafts.fairs.serializers import FairDetailModelSerializer



class FairPostModelSerializer(serializers.ModelSerializer):
    """FairPost model serializer"""
    class Meta:
        """class meta"""
        model = FairPost
        fields = (
            "id",
            "fair",
            "post",
        )

    def validate(self, data):
        fair = data['fair']
        post = data['post']

        if not Participant.objects.filter(fair=fair,user=post.user,active=True).exists():
            raise serializers.ValidationError(_("The user of the post is not a participant in the fair"))

        qs = FairPost.objects.filter(fair=fair,post=post,active=True)
        if qs.exists():
            raise serializers.ValidationError(_("Post is already on fair"))



        data['user'] = post.user
        return data

    def create(self, data):
        instance = FairPost.objects.create(**data)
        return instance

class FairPostDetailModelSerializer(serializers.ModelSerializer):
    """FairPost model serializer"""
    post = PostDetailModelSerializer(many=False)
    fair = FairDetailModelSerializer(many=False)

    class Meta:
        """class meta"""
        model = FairPost
        fields = (
            "id",
            "fair",
            "post",
        )