{{ config(materialized="view") }}


with
    measurements_data as (
        select * from {{ source("raw", "openaq_data_2019_2024") }}
    ),
    stg_openaq_measurements as (
        select
            cast(measurement_id as int) as measurement_id,
            cast(timestamp as datetime) as measurement_date,
            cast(location_id as int) as location_id,
            cast(parameter_id as int) as parameter_id,
            cast(measurement_average as Decimal) as measurement_average,
            cast(measurement_count as int) as measurement_count,
        from measurements_data
    )
select *
from stg_openaq_measurements

{% if var("is_test_run", default=true) %} limit 1000 {% endif %}
