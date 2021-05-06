from django_typomatic import ts_interface

from rest_framework.serializers import CharField, DateField, ModelSerializer, Serializer

from app.api.serializers import CountrySerializer
from immigration.models import ProcessStep, Route

_TS_INTERFACE_GROUP = "immigration"


@ts_interface(context=_TS_INTERFACE_GROUP)
class OccupationSerializer(Serializer):
    name = CharField()


@ts_interface(context=_TS_INTERFACE_GROUP)
class MoveSerializer(Serializer):
    host_country = CountrySerializer()
    target_entry_date = DateField(required=False, allow_null=True)
    target_exit_date = DateField(required=False, allow_null=True)


@ts_interface(context=_TS_INTERFACE_GROUP)
class RouteSerializer(ModelSerializer):
    host_country = CountrySerializer()

    class Meta:
        model = Route
        fields = "__all__"


@ts_interface(context=_TS_INTERFACE_GROUP)
class ProcessStepSerializer(ModelSerializer):
    class Meta:
        model = ProcessStep
        fields = "__all__"


@ts_interface(context=_TS_INTERFACE_GROUP)
class ProcessSerializer(Serializer):
    route = RouteSerializer()
    steps = ProcessStepSerializer(many=True)
