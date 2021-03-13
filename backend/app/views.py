from django.http import JsonResponse

from app.models import PersonImmigrationTask


def person_immigration_tasks(request):
    qs = PersonImmigrationTask.objects.values(
        "person__first_name",
        "person__last_name",
        "person__home_country",
        "case_type",
        "created_at",
        "current_status",
        "host_country",
        "progress",
        "service",
        "target_entry_date",
    )
    return JsonResponse(list(qs), safe=False)
