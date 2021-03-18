from django.db import models


class Employee(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    home_country = models.CharField(max_length=128)


class Case(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.deletion.CASCADE)
    case_type = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now=True)
    current_status = models.CharField(max_length=128)
    host_country = models.CharField(max_length=128)
    progress = models.FloatField()
    service = models.CharField(max_length=128)
    target_entry_date = models.DateField()
