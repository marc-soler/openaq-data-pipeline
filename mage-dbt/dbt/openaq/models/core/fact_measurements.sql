{{ config(materialized="table") }}


with
    stg_openaq_measurements as (
        select * from {{ source("stg", "stg_openaq_measurements") }}
    )
select *
from stg_openaq_measurements

{% if var("is_test_run", default=true) %} limit 1000 {% endif %}
