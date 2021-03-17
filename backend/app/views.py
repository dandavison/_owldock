from django.http import JsonResponse

from app.models import PersonImmigrationTask


def person_immigration_task(request, task_id: int):
    qs = PersonImmigrationTask.objects.filter(id=task_id).values(
        "id",
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
    return JsonResponse(list(qs)[0], safe=False)


def person_immigration_tasks(request):
    qs = PersonImmigrationTask.objects.values(
        "id",
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
