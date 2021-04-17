from django.core.exceptions import FieldDoesNotExist
from django.db.models import ForeignKey, Model
from django_tools.middlewares.ThreadLocal import _thread_locals

from owldock.models.fields import UUIDPseudoForeignKeyField

from clint.textui.colored import red, blue, green


class PrefetchCacheAwareSerializerMixin:
    """
    A mixin that fills a cache with prefetched objects before serializing.
    """

    def to_representation(self, instance):
        if not isinstance(instance, _SerializingProxy):
            instance = _SerializingProxy(instance)
        return super().to_representation(instance)

    @classmethod
    def set_prefetch_cache(cls, prefetch_cache: dict) -> None:
        _thread_locals.prefetch_cache = prefetch_cache


class _SerializingProxy:
    """
    A proxy object used during serialization by _PrefetchCacheAwareSerializerMixin.
    """

    def __init__(self, instance: Model):
        self._instance = instance

    def __getattr__(self, name):
        """
        Return an appropriate object for instance.<name> during serialization.

        If `name` is a ForeignKey or UUIDPseudoForeignKey field, then the
        referenced object should be stored under a key of the form
        (<referenced_model>, <referenced_row_id_or_uuid>). Return the referenced
        object from the cache, wrapped in _SerializingProxy.

        If `name` refers to a many-to-many relationship, then there should be a
        key in the cache of the form (instance.<model>, instance.uuid, <name>)
        holding a list of objects. Return this list, wrapping each element in
        _SerializingProxy.

        Otherwise, just return the attribute value.
        """

        instance = self.__dict__["_instance"]
        if not getattr(_thread_locals, "prefetch_cache", {}):
            return getattr(instance, name)

        object_cache = _thread_locals.prefetch_cache["object_cache"]
        related_objects_cache = _thread_locals.prefetch_cache["related_objects_cache"]

        model_cls = instance._meta.model

        # print(blue(f"{model_cls.__name__}.{name}"))

        # Check if name is a UUID pseudo foreign key.
        uuid_field_name = f"{name}_uuid"
        try:
            field = instance._meta.get_field(uuid_field_name)
        except FieldDoesNotExist:
            pass
        else:
            if isinstance(field, UUIDPseudoForeignKeyField):
                uuid = instance.__dict__[uuid_field_name]
                msg = (
                    f"Cache %s (UUID): {model_cls.__name__}.{name} => "
                    f"{(field.to, uuid)}"
                )
                try:
                    related_instance = object_cache[field.to, uuid]
                except KeyError:
                    print(red(msg % "miss"))
                else:
                    print(green(msg % "hit"))
                    return _SerializingProxy(related_instance)

        # Check if name is a foreign key.
        try:
            field = instance._meta.get_field(name)
        except FieldDoesNotExist:
            pass
        else:
            if isinstance(field, ForeignKey):
                id = instance.__dict__[f"{field.name}_id"]
                msg = (
                    f"Cache %s (FK): {model_cls.__name__}.{name} => "
                    f"{(field.related_model, id)}"
                )
                try:
                    related_instance = object_cache[field.related_model, id]
                except KeyError:
                    print(red(msg % "miss"))
                else:
                    print(green(msg % "hit"))
                    return _SerializingProxy(related_instance)

        # Check if `name` is a related objects manager.
        # If so then we hope to find the list of related objects in the cache.
        related_object_fields = [obj.field for obj in instance._meta.related_objects]
        val = getattr(instance, name)
        if hasattr(val, "field") and val.field in related_object_fields:
            msg = (
                f"Cache %s (Related objects): {model_cls.__name__}.{name} => "
                f"{(model_cls, instance.uuid, name)}"
            )
            try:
                related_instances = related_objects_cache[
                    model_cls, instance.uuid, name
                ]
            except KeyError:
                print(red(msg % "miss"))
            else:
                print(green(msg % "hit"))
                return [_SerializingProxy(obj) for obj in related_instances]

        return val
