-- CREATE SCHEMA geostore (set the password you prefer)
/*CREATE user geostore LOGIN PASSWORD 'geostore' NOSUPERUSER INHERIT NOCREATEDB NOCREATEROLE;*/

/*CREATE DATABASE geostore*/;
\c geostore;

CREATE SCHEMA IF NOT EXISTS geostore;

GRANT USAGE ON SCHEMA geostore TO geostore ;
GRANT ALL ON SCHEMA geostore TO geostore ;

alter user geostore set search_path to geostore , public;
