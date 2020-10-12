from model.statistics_summary import StatisticSummary
from store import Database
import numpy as np


def statistics_transform(data):
    row, col = data.shape
    districts = data.id.unique()
    indicators = int(col) - 7  # TODO:Improve calculation
    facilities = data.facility_name.unique()

    # total cases reported 2020
    total_opd = data.pivot_table(
        columns="year", values="OPD attendance", aggfunc=np.sum
    )
    total_dpt3 = data.pivot_table(columns="year", values="DPT3 (all)", aggfunc=np.sum)
    total_sam = data.pivot_table(
        columns="year", values="Number of SAM admissions", aggfunc=np.sum
    )
    total_first_anc_women = data.pivot_table(
        columns="year", values="1st ANC Visits", aggfunc=np.sum
    )
    total_tested_hiv_positive = data.pivot_table(
        columns="year", values="Tested HIV positive", aggfunc=np.sum
    )
    total_malaria_cases = data.pivot_table(
        columns="year", values="Malaria tests", aggfunc=np.sum
    )
    total_tb = data.pivot_table(
        columns="year", values="TB cases registered", aggfunc=np.sum
    )

    avg_opd = round(total_opd[2019].mean(), 2)
    avg_dpt3 = round(total_dpt3[2019].mean(), 2)
    avg_sam = round(total_sam[2019].mean(), 2)
    avg_first_anc_women = round(total_first_anc_women[2019].mean(), 2)
    avg_tested_hiv_positive = round(total_tested_hiv_positive[2019].mean(), 2)
    avg_malaria_cases = round(total_malaria_cases[2019].mean(), 2)
    avg_tb = round(total_tb[2019].mean(), 2)

    data_out = {
        "districts": len(districts),
        "indicators": indicators,
        "facilities": len(facilities),
        "avg_opd": avg_opd,
        "avg_dpt3": avg_dpt3,
        "avg_sam": avg_sam,
        "avg_first_anc_women": avg_first_anc_women,
        "avg_tested_hiv_positive": avg_tested_hiv_positive,
        "avg_malaria_cases": avg_malaria_cases,
        "avg_tb": avg_tb,
    }

    return data_out


statistics = StatisticSummary(data=statistics_transform(Database().data_raw))
