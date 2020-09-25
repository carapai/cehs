# Data csv download links

import xlsxwriter
import pandas as pd
import base64
import io


def download_file(dict_of_st):

    with pd.ExcelWriter('./coc-dashboard/assets/cehs.xlsx',engine='xlsxwriter') as writer:  
        for df_name, df in dict_of_st.items():
            if len(df_name) > 31:
                df_name = df_name[:30]
            df.to_excel(writer, sheet_name=df_name)

# Methodology section


def meth_data(date):
    meth_data = [
        {
            'sub_title': "Date of download",
            'body': f"The data shown here was last fetched from DHIS2 on {date}.",
            'list_data': []
        },
        {
            'sub_title': 'Choice of Indicators',
            'body': "We focus on a key set of indicators as advised by experts and described in WHO's list of priority indicators. For simplicity of interpretation and time comparison, we focus on absolute numbers rather than calculated indicators. ",
            'list_data': []
        },
        {
            'sub_title': 'Outlier Exclusion',
            'body': "We exclude outliers at facility level - for a given facility and indicator, we look at all data points available since January 2018 and replace all data points identified as outliers by the sample's median. We give two options for outlier exclusion: ",
            'list_data': [
                "A standard deviation-based approach, where all points more than three standard deviations away from the mean are considered outliers. This approach is best suited for 'cleaner', normally distributed data.",
                "An interquartile range-based approach, using Tukey's fences method with k=3, which fits a broader range of data distributions but is also more stringent, and hence best suited for 'messier' data.",
            ]
        },
        {
            'sub_title': 'Reporting Rates ',
            'body': "We provide two layers of information on reporting rate:",
            'list_data': [
                "A form-specific indicator - the percentage of facilities that reported on their 105:1 form out of those expected to report. This is similar to the reporting rates displayed on the DHIS2 system.",
                "An indicator-specific indicator - the percentage of facilities that reported a posistive number for the selected indicator out of all facilities that have submitted their 105:1 form. This provides added information on how otherwise reporting facilities report on this specific indicator. "
            ]
        }

    ]
    return meth_data
