from immigration.models import IssuedDocumentType


def describe_issued_documents():
    for idt in IssuedDocumentType.objects.all():
        print(idt)
        for id in idt.issueddocument_set.select_related("process_step__host_country"):
            print(
                f"    {id.id} {id.process_step.host_country.name} : "
                f"{id.process_step.name} ({id.process_step.id}) "
                f"{id.proves_right_to_enter} {id.proves_right_to_reside} {id.proves_right_to_work}"
            )
        print()
