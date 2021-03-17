from rest_framework import viewsets

from app.models import PersonImmigrationTask
from app.serializers import PersonImmigrationTaskSerializer


class PersonImmigrationTaskViewSet(viewsets.ModelViewSet):
    queryset = PersonImmigrationTask.objects.all()
    serializer_class = PersonImmigrationTaskSerializer
