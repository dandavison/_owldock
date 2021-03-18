from django.contrib import admin

from .models import Employee
from .models import ImmigrationTask

admin.site.register(Employee)
admin.site.register(ImmigrationTask)
