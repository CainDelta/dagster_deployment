
{{ config(alias='AIRPORT_METRICS',materialized='view',schema="PUBLIC") }}

select count(*) num_trips, extract (hour from tpep_pickup_datetime) as hour,avg(trip_distance) as avg_distance, avg(fare_amount) as avg_fare
from {{ref('airport_trips')}}
group by 2
