from django.contrib import admin

from .models import Employee
from .models import Case

admin.site.register(Employee)
admin.site.register(Case)
