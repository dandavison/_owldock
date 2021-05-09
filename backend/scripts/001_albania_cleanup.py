from immigration.models import ProcessStep


def format_url(what, id, display):
    url = f"https://owldock.onrender.com/admin/immigration/{what}/{id}/change/"
    return f"[{display}]({url})"


def process_step_url(ps):
    return format_url("processstep", ps.id, ps.id)


def process_rule_set_url(prs):
    return format_url("processruleset", prs.id, prs.route.name)


ps_ids = [
    (1086, 1077),
    (1087, 1078),
    (1088, 1079),
    (1064, 1079),
]


rows = []
rows.append(("Process Step", "Name", "Country", "Process Rule Set"))
rows.append(("------------", "----", "-------", "----------------"))
for generic_id, canonical_id in ps_ids:
    generic = ProcessStep.objects.get(id=generic_id)
    canonical = ProcessStep.objects.get(id=canonical_id)
    assert generic.name == canonical.name
    for ps in [generic, canonical]:
        rows.append(
            (
                process_step_url(ps),
                ps.name,
                ps.host_country.name if ps.host_country else "(no country)",
                process_rule_set_url(ps.process_ruleset),
            )
        )
    rows.append(("", "", "", ""))


def make_markdown_row(row):
    return f"| {'| '.join(row)} |"


for row in rows:
    print(make_markdown_row(row))
