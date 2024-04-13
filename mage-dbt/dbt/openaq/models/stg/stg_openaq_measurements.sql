{{
    config(
        materialized='view'
    )
}}


with measurements_data as (
    select * from {{ source('') }}
)