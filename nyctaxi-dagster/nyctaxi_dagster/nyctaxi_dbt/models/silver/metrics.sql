
{{ config(alias='METRICS',materialized='table',schema="PUBLIC") }}

select vendorid, count(*) as num_of_rides, min(tpep_pickup_datetime) as first_ride,
max(tpep_pickup_datetime) as last_ride,avg(trip_distance) as avg_distance,
avg(fare_amount) as avg_fare
from {{source('raw','rides')}} a
group by 1
limit 10
