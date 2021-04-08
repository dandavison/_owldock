"""
https://docs.djangoproject.com/en/3.1/howto/custom-model-fields/

"""
from typing import Type

from django.db import models


class _ForwardManyToOneDescriptor:
    """
    From django/db/models/fields/related_descriptors.py:

    When a field defines a relation between two models, each model class provides an
    attribute to access related instances of the other model class (unless the
    reverse accessor has been disabled with related_name='+').

    Accessors are implemented as descriptors in order to customize access and
    assignment. This module defines the descriptor classes.

    Forward accessors follow foreign keys. Reverse accessors trace them back. For
    example, with the following models::

    class Parent(Model):
        pass

    class Child(Model):
        parent = ForeignKey(Parent, related_name='children')

    ``child.parent`` is a forward many-to-one relation. ``parent.children`` is a
    reverse many-to-one relation.
    """

    def __init__(self, field_with_rel):
        self.field = field_with_rel

    def __get__(self, instance, cls=None):
        """
        Get the related instance through the forward relation.

        With the example above, when getting ``child.parent``:

        - ``self`` is the descriptor managing the ``parent`` attribute
        - ``instance`` is the ``child`` instance
        - ``cls`` is the ``Child`` class (we don't need it)
        """
        return self.field.to.objects.get(
            **{self.field.to_field: getattr(instance, self.field.name)}
        )


class UUIDPseudoForeignKeyField(models.UUIDField):
    """
    A UUID field that is intended to be used as a pseudo-foreign key to a field
    in a table in a different database. Accordingly, it always creates an index.
    A target model class (`to`) must be supplied to indicate intent, although
    currently nothing is done with it. The target field (`to_field`) is an
    optional argument, defaulting to "id".
    """

    # Although we are creating a custom model field here, this is intended to be
    # a very minor extension of UUIDField. What this field does, beyond what
    # UUIDField does, is:
    #
    # Suppose it is used like this:
    #
    # parent_id = UUIDPseudoForeignKeyField(Parent)
    #
    # Then, a python property named 'parent' will be added to the model instance
    # object. This property, when accessed, will attempt to execute
    # Parent.objects.get(id=self.parent_id)
    #
    # Nothing else is intended to change.

    forward_related_accessor_class = _ForwardManyToOneDescriptor

    def __init__(
        self,
        to: Type[models.Model],
        *args,
        to_field="id",
        db_index=True,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.to = to
        self.to_field = to_field

    def deconstruct(self):
        # https://docs.djangoproject.com/en/3.1/howto/custom-model-fields/#field-deconstruction
        name, path, args, kwargs = super().deconstruct()
        args = [self.to] + list(args)
        kwargs.setdefault("to_field", "id")
        kwargs.setdefault("db_index", True)
        return name, path, args, kwargs

    def contribute_to_class(self, cls, name, **kwargs):
        super().contribute_to_class(cls, name, **kwargs)
        forward_related_accessor_name, sep, suffix = self.name.rpartition("_id")
        assert sep == "_id" and not suffix, f"Expected {self.name} to end in '_id'"
        setattr(
            cls,
            forward_related_accessor_name,
            self.forward_related_accessor_class(self),
        )
