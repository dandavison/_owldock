from rest_framework import permissions
from rest_framework import viewsets

from app.models import ImmigrationTask
from app.serializers import ImmigrationTaskSerializer


class ImmigrationTaskViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.DjangoObjectPermissions]

    queryset = ImmigrationTask.objects.all()
    serializer_class = ImmigrationTaskSerializer
