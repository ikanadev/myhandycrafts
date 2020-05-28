""""StorePost serialisers."""
#django
from django.utils.translation import ugettext_lazy as _

# Django REST Framework
from rest_framework import serializers

# models
from myhandycrafts.posts.models import StorePost


# serializer
from myhandycrafts.posts.serializers import PostDetailModelSerializer
from myhandycrafts.stores.serializers import StoreDetailModelSerializer



class StorePostModelSerializer(serializers.ModelSerializer):
    """StorePost model serializer"""
    class Meta:
        """class meta"""
        model = StorePost
        fields = (
            "id",
            "store",
            "post",
        )

    def validate(self, data):
        store = data['store']
        post = data['post']

        if store.user != post.user :
            raise serializers.ValidationError(_("The user of the post is not a the usesr of store"))

        qs = StorePost.objects.filter(store=store,post=post,active=True)
        if qs.exists():
            raise serializers.ValidationError(_("Post is already on store"))



        data['user'] = post.user
        return data

    def create(self, data):
        instance = StorePost.objects.create(**data)
        return instance

class StorePostDetailModelSerializer(serializers.ModelSerializer):
    """StorePost model serializer"""
    post = PostDetailModelSerializer(many=False)
    store = StoreDetailModelSerializer(many=False)

    class Meta:
        """class meta"""
        model = StorePost
        fields = (
            "id",
            "store",
            "post",
        )