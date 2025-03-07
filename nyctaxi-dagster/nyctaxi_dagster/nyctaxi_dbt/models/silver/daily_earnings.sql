
{{ config(alias='DAILY_EARNINGS',materialized='table',schema="PUBLIC") }}

select tpep_pickup_datetime::date as date,sum(fare_amount) as total_fares
from {{source('raw','rides')}}
group by 1
order by 1 desc
