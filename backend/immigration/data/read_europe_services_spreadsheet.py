import json
import sys
from typing import Dict, List, Optional

import pandas as pd


RouteName = str
Country = str
ServiceItemDescription = str
CountryData = Dict[RouteName, List[ServiceItemDescription]]


def read_sheets(path: str) -> Dict[Country, CountryData]:
    xlsx = pd.ExcelFile(path)
    data = {}
    for sheet_name in xlsx.sheet_names:
        df = pd.read_excel(xlsx, sheet_name)
        try:
            data[sheet_name] = read_sheet(df)
        except Exception as exc:
            print(f"Error reading sheet {sheet_name}", file=sys.stderr)
            print(f"{exc.__class__.__name__}: {exc}", file=sys.stderr)
    return data


def read_sheet(df: pd.DataFrame) -> CountryData:
    assert list(df.columns[:2]) == ["Immigration category", "Service description"]
    data: CountryData = {}
    current_route = None
    for row in df.itertuples(index=False):
        route, service = map(clean_string, row[:2])
        if not service:
            assert route and route.startswith("Hourly rate for")
            return data
        if route:
            current_route = route
        assert current_route
        data.setdefault(current_route, []).append(service)
    assert False


def clean_string(s: str) -> Optional[str]:
    if not pd.isna(s):
        assert s
        return s.replace("\xa0", " ").strip()
    else:
        return None


if __name__ == "__main__":
    data = read_sheets("./Europe services spreadsheet 05 May.xlsx")
    with open("Europe services spreadsheet 05 May.json", "w") as fp:
        json.dump(data, fp, indent=2, sort_keys=True)
