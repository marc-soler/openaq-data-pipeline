{{ config(materialized="view") }}


with
    measurements_data as (
        select * from {{ source("mage_openaq", "openaq_data_2019_2024") }}
    ),
    stg_openaq_measurements as (
        select
            measurement_id,
            location_id,
            parameter_id,
            measurement_average,
            measurement_count
        from measurements_data
    )
select *
from stg_openaq_measurements

{% if var("is_test_run", default=true) %} limit 1000 {% endif %}
