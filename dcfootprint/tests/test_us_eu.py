"""US/EU inputs: capacity-basis classifier, EU extraction totals, Ember normalisation."""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from dcfootprint.io import ember
from dcfootprint.io.us_facilities import classify_basis

ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize("recorded,notes,expected", [
    (5.0, "Operator states 5 MW of IT capacity across two halls.", "it"),
    (21.5, "21.5 MW critical IT load; 32 MW utility power to the site.", "it"),
    (6.0, "3 MW immediately available out of 6 MW total utility power and generator capacity.", "facility"),
    (80.0, "the property has 80 MW of total utility power", "facility"),
    (80.0, "the property totals 80 MW power capacity", "unspecified"),   # ambiguous wording: not facility by rule
    (12.0, "Opened in 2019; expansion planned.", "unspecified"),
    (4.0, "", "unspecified"),
])
def test_classify_basis(recorded, notes, expected):
    assert classify_basis(recorded, notes) == expected


def test_eu_extraction_reproduces_report_totals():
    eu = pd.read_csv(ROOT / "dcfootprint" / "config" / "eu_member_state_2023.csv")
    assert len(eu) == 27 and eu["reported_energy_gwh"].notna().sum() == 21
    # Table 22 of the report: EU totals of all reporting datacentres
    assert eu["reported_it_mw"].sum() == pytest.approx(3738.86, abs=0.02)
    assert eu["reported_energy_gwh"].sum() == pytest.approx(14088.0, abs=0.02)
    assert eu["reported_water_input_m3"].sum() == pytest.approx(6223391, abs=0.5)
    assert eu["reporting_n_dc"].sum() == 770 and eu["est_n_dc"].sum() == 2161      # Table 13 TOTAL row


@pytest.mark.parametrize("region,year,n_zones,national", [("India", 2024, 36, "India Total"),
                                                          ("US", 2024, 52, "US Total"),
                                                          ("EU", 2023, 27, "EU Total")])
def test_ember_regions_coherent(region, year, n_zones, national):
    raw = ember.load_raw(region)
    assert ember.national_of(raw) == national
    z = ember.zones_of(raw)
    assert len(z) == n_zones
    ci = ember.zone_month_ci(raw, year, "state")
    assert (ci["ci_source"] == "ember_state").all()
    sh = ember.zone_month_fuel_shares(raw, year, "state")
    assert np.allclose(sh.groupby(["zone_id", "month"])["share"].sum(), 1.0)
    gen = raw[(raw["Variable"] == "Total Generation") & (raw["Unit"] == "GWh") & (raw["date"].dt.year == year)]
    g = gen.pivot_table(index="date", columns="State", values="Value")
    assert float(((g[z].sum(axis=1) - g[national]).abs() / g[national]).max()) < 0.01   # zones sum to the aggregate


def test_india_gem_state_of_record_unchanged():
    """The region refactor must leave India's GEM state assignment as in round 3."""
    from dcfootprint.io.gem import region_plants
    p = region_plants("India")
    assert len(p) == 5764
    assert p["state_source"].value_counts().to_dict() == {"gadm_agrees": 5717, "gadm": 43, "override": 3, "ambiguous": 1}
