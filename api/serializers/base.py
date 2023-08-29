from rest_framework import serializers


class BaseSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.SerializerMethodField()

    def get_id(self, instance):
        return instance.id

    class Meta:
        ordering = ['id']
        model = None
