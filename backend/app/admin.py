from django.contrib import admin

from .models import Applicant
from .models import Case

admin.site.register(Applicant)
admin.site.register(Case)
