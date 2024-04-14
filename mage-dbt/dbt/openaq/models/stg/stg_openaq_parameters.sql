{{ config(materialized="view") }}


with
    parameters_data as (
        select * from {{ source("raw", "openaq_data_2019_2024") }}
    ),
    stg_openaq_parameters as (
        select distinct
            cast(parameter_id as int) as parameter_id,
            parameter_code,
            parameter_name,
            description,
            unit
        from parameters_data
    )
select *
from stg_openaq_parameters

{% if var("is_test_run", default=true) %} limit 1000 {% endif %}
