
{{ config(alias='TOP_PICKUP_LOCATIONS',materialized='table',schema="PUBLIC") }}

select a.pulocationid,tpep_pickup_datetime::date as date, count(*) as num_pickups,sum(fare_amount) as total_amount,
c.total_fares as total_daily_fare,sum(fare_amount)/c.total_fares*100 as pct_total_daily_fare
from {{source('raw','rides')}} a
inner join {{ref('busiest_pickups')}} b
on a.pulocationid  = b.pulocationid
left join {{ref('daily_earnings')}} c
on tpep_pickup_datetime::date = c.date
group by 1,2,5
order by 2 desc
