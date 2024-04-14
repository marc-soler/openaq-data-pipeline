{{ config(materialized="table") }}


with
    stg_openaq_parameters as (
        select * from {{ source("stg", "stg_openaq_parameters") }}
    )
select *
from stg_openaq_parameters

{% if var("is_test_run", default=true) %} limit 1000 {% endif %}
