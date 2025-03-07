{{ config(alias='AIRPORT_TRIPS',materialized='table',schema="PUBLIC") }}

select *  from {{source('raw','rides')}}
where airport_fee > 0
