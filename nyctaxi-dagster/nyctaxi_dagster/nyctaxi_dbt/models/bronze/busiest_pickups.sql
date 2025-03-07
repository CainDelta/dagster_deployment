{{ config(alias='BUSIEST_PICKUPS',materialized='table',schema="PUBLIC") }}

select pulocationid, count(*) as num_pickups from {{source('raw','rides')}}
group by 1
order by 2 desc
limit 10
