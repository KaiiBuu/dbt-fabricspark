import pandas as pd
import os


def model(dbt, session):
    dbt.config(materialized="table", schema="lh_dp_silver.hr", tags="sgr_location_manual")
    workspace_id = dbt.config.get('workspace_id')
    lh_bronze_id = dbt.config.get('lh_bronze_id')

    file_path = 'Files/dp_hr/static_file/report_Location_SG.xlsx'

    location_df = pd.read_excel(f'abfss://{workspace_id}@onelake.dfs.fabric.microsoft.com/{lh_bronze_id}/{file_path}')
    location_df = spark.createDataFrame(location_df)
    location_df = location_df.toDF('location_group', 'external_code', 'status', 'location_name', 'county', 'province',
                                   'group_name')
    location_df = location_df.dropDuplicates(["external_code"])

    return location_df