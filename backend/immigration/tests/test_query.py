from datetime import timedelta
from unittest.mock import patch

from django.utils import timezone

from app.api.serializers import MoveSerializer
from immigration.models import Location, Move
from immigration.query import get_processes


def test_eu_to_greece_move_query(
    greece_local_hire_article_17_rule_set,
    greece_eu_eea_swiss_national_registration_rule_set,
    greece_technical_assignment_article_18_route_rule_set,
    brazil,
    france,
    greece,
):
    rule_sets = [
        greece_local_hire_article_17_rule_set,
        greece_eu_eea_swiss_national_registration_rule_set,
        greece_technical_assignment_article_18_route_rule_set,
    ]

    eu_to_greece_move = Move(nationalities=[france], host_country=greece)
    eu_to_greece_move_data = MoveSerializer(eu_to_greece_move).data

    with patch("immigration.query._get_all_process_rulesets", return_value=rule_sets):

        assert [p.route for p in get_processes(eu_to_greece_move_data)] == [
            greece_eu_eea_swiss_national_registration_rule_set.route
        ]


def test_non_eu_to_greece_host_payroll_move_query(
    greece_local_hire_article_17_rule_set,
    greece_eu_eea_swiss_national_registration_rule_set,
    greece_technical_assignment_article_18_route_rule_set,
    brazil,
    france,
    greece,
):
    rule_sets = [
        greece_local_hire_article_17_rule_set,
        greece_eu_eea_swiss_national_registration_rule_set,
        greece_technical_assignment_article_18_route_rule_set,
    ]

    non_eu_to_greece_host_payroll_move = Move(
        nationalities=[brazil],
        host_country=greece,
        payroll_location=Location.HOST_COUNTRY,
    )
    non_eu_to_greece_host_payroll_move_data = MoveSerializer(
        non_eu_to_greece_host_payroll_move
    ).data

    with patch("immigration.query._get_all_process_rulesets", return_value=rule_sets):

        assert [
            p.route for p in get_processes(non_eu_to_greece_host_payroll_move_data)
        ] == [greece_local_hire_article_17_rule_set.route]


def test_non_eu_to_greece_home_payroll_move_query(
    greece_local_hire_article_17_rule_set,
    greece_eu_eea_swiss_national_registration_rule_set,
    greece_technical_assignment_article_18_route_rule_set,
    brazil,
    france,
    greece,
):
    rule_sets = [
        greece_local_hire_article_17_rule_set,
        greece_eu_eea_swiss_national_registration_rule_set,
        greece_technical_assignment_article_18_route_rule_set,
    ]
    now = timezone.now()
    non_eu_to_greece_home_payroll_move = Move(
        nationalities=[brazil],
        host_country=greece,
        payroll_location=Location.HOME_COUNTRY,
        target_entry_date=now,
        target_exit_date=now + timedelta(weeks=12),
    )
    non_eu_to_greece_home_payroll_move_data = MoveSerializer(
        non_eu_to_greece_home_payroll_move
    ).data

    with patch("immigration.query._get_all_process_rulesets", return_value=rule_sets):

        assert [
            p.route for p in get_processes(non_eu_to_greece_home_payroll_move_data)
        ] == [greece_technical_assignment_article_18_route_rule_set.route]
