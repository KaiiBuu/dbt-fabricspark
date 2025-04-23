{{ config(
    schema='lh_dp_bronze.dbt_mat',
    file_format = 'delta',
    materialized='incremental',
    unique_key=['id', 'external_id'],
    incremental_strategy = 'merge',
    tmp_schema = 'lh_dp_bronze.dbt_mat'
) }}

SELECT
    id,
    external_id,
    name,
    date_join,
    email,
    rank,
    updated_at,
    from_utc_timestamp(current_timestamp(), 'Asia/Bangkok') as dbt_updated_at
FROM {{ source('dbt_mat','stg_people_info') }}
{% if is_incremental() %}
    WHERE updated_at >= (SELECT COALESCE(MAX(updated_at), '1900-01-01') FROM {{ this }})
{% endif %}