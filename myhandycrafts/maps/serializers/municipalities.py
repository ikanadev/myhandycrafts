"""Municipality serializer."""

# Django REST Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# Model
from myhandycrafts.maps.models import Municipality,Province


class MunicipalityModelSerializer(serializers.ModelSerializer):
    """Municipality model serializer."""
    name = serializers.CharField(min_length=2,
                                 max_length=32,
                                 validators=[UniqueValidator(
                                     queryset=Municipality.objects.filter(
                                         is_deleted=False
                                     )
                                 )]
                                 )

    class Meta:
        model = Municipality
        fields = (
            'id',
            'departament',
            'province',
            'name',
            'description',
        )

        read_only_fields=(
            'departament',
        )

    def validate_province(self,province):

        if province.is_deleted:
            raise serializers.ValidationError("Invalid pk \"{}\" - object "
                                              "does not exist".format(
                                                            province.pk))
        if province.departament.is_deleted:
            raise serializers.ValidationError("Invalid pk \"{}\" - object "
                                              "does not exist".format(
                                                            province.pk))

        self.context['province']=province
        self.context['departament'] = province.departament
        return province

    def create(self, data):
        province = self.context['province']
        data.pop('province')
        municipality = Municipality.objects.create(
            **data,
            departament=self.context['departament'],
            province=self.context['province']
        )
        return municipality

    def update(self, instance, data):
        departament = self.context['departament']
        province = self.context['province']

        instance.departament = departament
        instance.province = province
        return super(MunicipalityModelSerializer,self).update(instance,data)

