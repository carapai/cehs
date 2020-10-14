from store import (
    filter_df_by_dates,
    filter_by_district,
    get_district_sum,
    get_national_sum,
    get_percentage,
    get_sub_dfs,
    month_order,
    timeit,
    Database,
    static,
)

import pandas as pd

# CARD 1


@timeit
def scatter_country_data(*, outlier, indicator, indicator_group, **kwargs):

    # dfs, static,

    db = Database()

    df = db.filter_by_policy(outlier)

    df = db.filter_by_indicator(df, indicator)

    df_country = get_percentage(
        df,
        static.get("population data"),
        static.get("target population type"),
        indicator_group,
        indicator,
        all_country=True,
    )

    # df_country.rename(
    #     columns={
    #         indicator: get_new_indic_name(
    #             static.get("indicator_groups"), indicator, indicator_group
    #         )
    #     },
    #     inplace=True,
    # )

    return df_country


# CARD 2


@timeit
def map_bar_country_dated_data(
    *,
    outlier,
    indicator,
    indicator_group,
    target_year,
    target_month,
    reference_year,
    reference_month,
    **kwargs,
):

    db = Database()

    df = db.filter_by_policy(outlier)

    df = db.filter_by_indicator(df, indicator)

    data_in = filter_df_by_dates(
        df, target_year, target_month, reference_year, reference_month
    )

    data_in = get_percentage(
        data_in,
        static.get("population data"),
        static.get("target population type"),
        indicator_group,
        indicator,
    )

    data_in.reset_index(inplace=True)

    # TODO updat teh filter by data function so that this step is no longer needed

    min_date = data_in.date.min()
    max_date = data_in.date.max()

    mask = (data_in.date == min_date) | (data_in.date == max_date)

    data_in = data_in[mask]

    data_in = data_in.groupby(by=["id", "date"], as_index=False).agg({indicator: "sum"})

    data_in["year"] = data_in.date.apply(lambda x: x.year)

    data_in = data_in.pivot_table(columns="year", values=indicator, index="id")

    data_in[indicator] = (
        (data_in[int(target_year)] - data_in[int(reference_year)])
        / data_in[int(reference_year)]
        * 100
    )
    data_in[indicator] = data_in[indicator].apply(lambda x: round(x, 2))

    data_in = data_in[[indicator]].reset_index()
    data_in["id"] = data_in["id"].astype(str)
    data_in = data_in.set_index("id")
    data_out = data_in[~pd.isna(data_in[indicator])]

    # data_out.rename(
    #     columns={
    #         indicator: get_new_indic_name(
    #             static.get("indicator_groups"), indicator, indicator_group
    #         )
    #     },
    #     inplace=True,
    # )

    return data_out


# CARD 3


@timeit
def scatter_district_data(*, outlier, indicator, indicator_group, district, **kwargs):

    db = Database()

    df = db.filter_by_policy(outlier)

    df = db.filter_by_indicator(df, indicator)

    df_district = filter_by_district(df, district)
    df_district = get_district_sum(df_district, indicator)
    df_district = get_percentage(
        df_district,
        static.get("population data"),
        static.get("target population type"),
        indicator_group,
        indicator,
    )

    # df_district.rename(
    #     columns={
    #         indicator: get_new_indic_name(
    #             static.get("indicator_groups"), indicator, indicator_group
    #         )
    #     },
    #     inplace=True,
    # )

    return df_district


# CARD 4


@timeit
def tree_map_district_dated_data(
    *,
    outlier,
    indicator,
    district,
    target_year,
    target_month,
    reference_year,
    reference_month,
    **kwargs,
):

    db = Database()

    df = db.filter_by_policy(outlier)

    df = db.filter_by_indicator(df, indicator)

    # TODO check how the date function works such that it shows only target date

    df_district_dated = filter_df_by_dates(
        df, target_year, target_month, reference_year, reference_month
    )

    df_district_dated = filter_by_district(df_district_dated, district)

    # df_district_dated.rename(
    #     columns={
    #         indicator: get_new_indic_name(static.get("indicator_groups"), indicator)
    #     },
    #     inplace=True,
    # )

    return df_district_dated


@timeit
def scatter_facility_data(*, outlier, indicator, district, facility, **kwargs):

    db = Database()

    df = db.filter_by_policy(outlier)

    df = db.filter_by_indicator(df, indicator)

    df = filter_by_district(df, district)

    # TODO Reorder such that its the one facility with the on selected data max value that shows

    if not facility:
        facility = df.facility_name[0]

    df = df[df.facility_name == facility].reset_index(drop=True)

    # df_facility.rename(
    #     columns={
    #         indicator: get_new_indic_name(static.get("indicator_groups"), indicator)
    #     },
    #     inplace=True,
    # )

    return df


# CARD 5


@timeit
def bar_reporting_country_data(*, indicator, **kwargs):

    db = Database()

    df = db.raw_data.get("value_rep")

    df = db.filter_by_indicator(df, indicator)

    # df.rename(
    #     columns={
    #         indicator: get_new_indic_name(static.get("indicator_groups"), indicator)
    #     },
    #     inplace=True,
    # )

    return df


# CARD 6


@timeit
def map_reporting_dated_data(
    *,
    indicator,
    target_year,
    target_month,
    reference_year,
    reference_month,
    **kwargs,
):

    db = Database()

    df = db.raw_data.get("value_rep")

    df = db.filter_by_indicator(df, indicator)

    df = filter_df_by_dates(
        df, target_year, target_month, reference_year, reference_month
    )

    # df.rename(
    #     columns={
    #         indicator: get_new_indic_name(static.get("indicator_groups"), indicator)
    #     },
    #     inplace=True,
    # )

    return df


# CARD 7


@timeit
def scatter_reporting_district_data(*, indicator, district, **kwargs):

    db = Database()

    df = db.raw_data.get("value_rep")

    df = db.filter_by_indicator(df, indicator)

    df_reporting_district = filter_by_district(df, district)

    # df_reporting_district.rename(
    #     columns={
    #         indicator: get_new_indic_name(static.get("indicator_groups"), indicator)
    #     },
    #     inplace=True,
    # )

    return df_reporting_district


# Indicator group grid


@timeit
def indicator_group(*, indicator_group, outlier, **kwargs):

    db = Database()

    df = db.filter_by_policy(outlier)

    # !FIXME when mutations and store are decoupled! !IMPORTANT

    groups = dict(
        MNCH=[
            "1st ANC Visits",
            "4th ANC Visits",
            "Maternity Admissions",
            "Deliveries in unit",
            "Deliveries in unit - live",
            "Deliveries in unit - fresh stillbirth",
            "Deliveries in unit - macerated stillbirth",
            "Newborn deaths",
            "Postnatal Visits",
        ],
        EPI=[
            "BCG (all)",
            "BCG (outreach)",
            "BCG (static)",
            "DPT1 (all)",
            "DPT1 (outreach)",
            "DPT1 (static)",
            "DPT3 (all)",
            "DPT3 (outreach)",
            "DPT3 (static)",
            "HPV1 (all)",
            "HPV1 (community)",
            "HPV1 (school)",
            "HPV2 (all)",
            "HPV2 (community)",
            "HPV2 (school)",
            "MR1 (all)",
            "MR1 (outreach)",
            "MR1 (static)",
            "PCV1 (all)",
            "PCV1 (outreach)",
            "PCV1 (static)",
            "PCV3 (all)",
            "PCV3 (outreach)",
            "PCV3 (static)",
            "TD1 (nonpregnant)",
            "TD1 (pregnant)",
            "TD2 (nonpregnant)",
            "TD2 (pregnant)",
            "TD3 (nonpregnant)",
            "TD3 (pregnant)",
            "TD4-5 (nonpregnant)",
            "TD4-5 (pregnant)",
        ],
        GENERAL=["OPD attendance", "IPD attendance"],
        HIV=[
            "Tested HIV",
            "Tested HIV positive",
            "HIV positive linked to care",
            "ANC tested HIV",
            "ANC tested HIV positive",
            "ANC initiated on ART",
            "Mat tested HIV",
            "Mat tested HIV positive",
            "Mat initiated on ART",
            "PNC tested HIV",
            "PNC tested HIV positive",
            "PNC initiated on ART",
        ],
        TB=["TB cases registered"],
        MAL=[
            "Malaria deaths",
            "Malaria cases treated",
            "Malaria cases",
            "Malaria tests",
        ],
        NUT=[
            "Number of doses of vitamin A distributed",
            "Number of SAM admissions",
            "Number of MAM admissions",
            "Low weight births",
        ],
    )

    df_groups = {"group": [], "indicator": []}
    for group, indicators in groups.items():
        df_groups["group"].extend([group] * len(indicators))
        df_groups["indicator"].extend(indicators)

    indicators_groups = pd.DataFrame(df_groups)

    indicators = list(
        indicators_groups[indicators_groups.group == indicator_group].indicator
    )

    columns_to_keep = db.index_columns + indicators
    df = df[columns_to_keep]

    return df
