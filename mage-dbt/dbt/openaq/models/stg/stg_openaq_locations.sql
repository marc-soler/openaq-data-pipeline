{{ config(materialized="view") }}


with
    locations_data as (
        select * from {{ source("raw", "openaq_data_2019_2024") }}
    ),
    stg_openaq_locations as (
        select distinct
            cast(location_id as int) as location_id,
            location_name,
            country,
            city,
            cast(latitude as Decimal) as latitude,
            cast(longitude as Decimal) as longitude
        from locations_data
    )
select *
from stg_openaq_locations

{% if var("is_test_run", default=true) %} limit 1000 {% endif %}
