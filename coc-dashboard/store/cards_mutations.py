from store import (
    filter_df_by_policy,
    filter_df_by_indicator,
    filter_df_by_dates,
    filter_by_district,
    get_district_sum,
    get_national_sum,
    get_percentage,
    get_sub_dfs,
    month_order,
    index_base_columns,
    timeit,
)

import pandas as pd

# CARD 1


def scatter_country_data(dfs, static, *, outlier, indicator, indicator_type, **kwargs):

    df = filter_df_by_policy(dfs, outlier)

    df = filter_df_by_indicator(df, indicator, persist_columns=index_base_columns)

    df_country = get_national_sum(df, indicator)

    df_country = get_percentage(
        df_country,
        static.get("population data"),
        static.get("target population type"),
        indicator_type,
        indicator,
        all_country=True,
    )

    return df_country


# CARD 2


def map_bar_country_dated_data(
    dfs,
    static,
    *,
    outlier,
    indicator,
    indicator_type,
    target_year,
    target_month,
    reference_year,
    reference_month,
    **kwargs,
):

    df = filter_df_by_policy(dfs, outlier)

    df = filter_df_by_indicator(df, indicator, persist_columns=index_base_columns)

    data_in = filter_df_by_dates(
        df, target_year, target_month, reference_year, reference_month
    )

    data_in = get_percentage(
        data_in,
        static.get("population data"),
        static.get("target population type"),
        indicator_type,
        indicator,
    )

    data_in.reset_index(inplace=True)

    # TODO updat teh filter by data function so that this step is no longer needed

    mask = (
        (data_in.year == int(reference_year)) & (data_in.month == reference_month)
    ) | ((data_in.year == int(target_year)) & (data_in.month == target_month))

    data_in = data_in[mask]

    data_in = data_in.groupby(by=["id", "year", "month"], as_index=False).agg(
        {indicator: "sum"}
    )
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

    return data_out


# CARD 3


def scatter_district_data(
    dfs, static, *, outlier, indicator, indicator_type, district, **kwargs
):
    df = filter_df_by_policy(dfs, outlier)

    df = filter_df_by_indicator(df, indicator, persist_columns=index_base_columns)

    df_district = filter_by_district(df, district)
    df_district = get_district_sum(df_district, indicator)
    df_district = get_percentage(
        df_district,
        static.get("population data"),
        static.get("target population type"),
        indicator_type,
        indicator,
    )

    return df_district


# CARD 4


def tree_map_district_dated_data(
    dfs,
    static,
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

    df = filter_df_by_policy(dfs, outlier)

    df = filter_df_by_indicator(df, indicator, persist_columns=index_base_columns)

    # TODO check how the date function works such that it shows only target date

    df_district_dated = filter_df_by_dates(
        df, target_year, target_month, reference_year, reference_month
    )

    df_district_dated = filter_by_district(df_district_dated, district)

    return df_district_dated


def scatter_facility_data(
    dfs, static, *, outlier, indicator, district, facility, **kwargs
):

    df = filter_df_by_policy(dfs, outlier)

    df = filter_df_by_indicator(df, indicator, persist_columns=index_base_columns)

    df_facility = filter_by_district(df, district)

    # TODO Reorder such that its the one facility with the on selected data max value that shows

    if facility:
        df_facility = df_facility[df_facility.facility_name == facility].reset_index(
            drop=True
        )
    else:
        df_facility = df_facility[
            df_facility.facility_name == df_facility.facility_name[0]
        ].reset_index(drop=True)

    return df_facility


# CARD 5


def bar_reporting_country_data(dfs, static, *, indicator, **kwargs):

    df_reporting = filter_df_by_policy(dfs, "Reporting")

    df_reporting = filter_df_by_indicator(
        df_reporting, indicator, persist_columns=index_base_columns
    )

    return df_reporting


# CARD 6


def map_reporting_dated_data(
    dfs,
    static,
    *,
    indicator,
    target_year,
    target_month,
    reference_year,
    reference_month,
    **kwargs,
):

    df_reporting = filter_df_by_policy(dfs, "Reporting")

    df_reporting = filter_df_by_indicator(
        df_reporting, indicator, persist_columns=index_base_columns
    )

    df_reporting_dated = filter_df_by_dates(
        df_reporting, target_year, target_month, reference_year, reference_month
    )

    return df_reporting_dated


# CARD 7


def scatter_reporting_district_data(dfs, static, *, indicator, district, **kwargs):

    df_reporting = filter_df_by_policy(dfs, "Reporting")

    df_reporting = filter_df_by_indicator(
        df_reporting, indicator, persist_columns=index_base_columns
    )

    df_reporting_district = filter_by_district(df_reporting, district)

    return df_reporting_district
