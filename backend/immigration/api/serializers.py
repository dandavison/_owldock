from django_typomatic import ts_interface

from rest_framework.serializers import CharField, Serializer


@ts_interface()
class OccupationSerializer(Serializer):
    name = CharField()
