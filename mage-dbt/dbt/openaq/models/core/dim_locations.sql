{{ config(materialized="table") }}


with
    stg_openaq_locations as (
        select * from {{ source("stg", "stg_openaq_locations") }}
    )
select *
from stg_openaq_locations

{% if var("is_test_run", default=true) %} limit 1000 {% endif %}
