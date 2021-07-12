from collections import defaultdict
from typing import List

from app import models as app_orm_models
from client import models as client_orm_models
from immigration import models as immigration_orm_models


def get_orm_models(
    client_contact: client_orm_models.ClientContact,
) -> List[client_orm_models.Applicant]:
    # TEMP: for demo purposes
    active_country_uuids = list(
        immigration_orm_models.Country.objects.filter(is_active=True).values_list(
            "uuid", flat=True
        )
    )
    applicants_qs = client_orm_models.Applicant.objects.filter(
        applicantnationality__country_uuid__in=active_country_uuids
    )
    # END
    applicants = list(applicants_qs.select_related("employer"))
    applicant_ids, user_uuids, home_country_uuids = [], [], []
    for a in applicants:
        applicant_ids.append(a.id)
        user_uuids.append(a.user_uuid)
        home_country_uuids.append(a.home_country_uuid)
    uuid2user = {
        u.uuid: u for u in app_orm_models.User.objects.filter(uuid__in=user_uuids)
    }
    applicant_ids__nationality_uuids = (
        client_orm_models.ApplicantNationality.objects.filter(
            applicant_id__in=applicant_ids
        ).values_list("applicant_id", "country_uuid")
    )
    uuid2country = {
        c.uuid: c
        for c in immigration_orm_models.Country.objects.filter(
            uuid__in=set(
                home_country_uuids
                + [uuid for _, uuid in applicant_ids__nationality_uuids]
            )
        )
    }
    applicant_id2nationalities = defaultdict(list)
    for applicant_id, country_uuid in applicant_ids__nationality_uuids:
        applicant_id2nationalities[applicant_id].append(uuid2country[country_uuid])

    for a in applicants:
        a._prefetched_user = uuid2user[a.user_uuid]
        a._prefetched_home_country = uuid2country[a.home_country_uuid]
        a._prefetched_nationalities = applicant_id2nationalities[a.id]
    return applicants
