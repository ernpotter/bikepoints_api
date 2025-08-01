USE DATABASE TIL_DATA_ENGINEERING;
USE SCHEMA JM_DES2_STAGING;

SELECT *
FROM bike_point_raw;

--- copying jenny's table / skipping loading data from s3 ----

CREATE OR REPLACE TABLE EP_DTHREE_STAGING.bike_point_raw AS
SELECT *
FROM JM_DES2_STAGING.bike_point_raw;

USE SCHEMA EP_DTHREE_STAGING;

SELECT *
FROM bike_point_raw;


--- unnest table ----
CREATE OR REPLACE TABLE bike_point_unnest1 AS 
SELECT 
    json:id::string as id
    , json:commonName::string as common_name
    , json:lat::float as latitude
    , json:lon::float as longitude
    , json:placeType::string as place_type
    , json:url::string as url
    , json:additionalProperties::variant as additional_properties
FROM bike_point_raw
--LIMIT 10
;

SELECT *
FROM bike_point_unnest1;

------- Table 1: Bike Point Fact Table -----------
CREATE OR REPLACE TABLE bike_point_location AS 
SELECT 
    TRIM(id) as id,
    TRIM(common_name) as common_name,
    latitude,
    longitude,
    TRIM(place_type) as place_type,
    TRIM(url) as url
FROM bike_point_unnest1;

------ Table 2: Current/Historic Properties -----------
CREATE OR REPLACE TABLE bike_point_unnest2 AS 
SELECT 
    id
    , value:key::varchar as key
    , value:value::varchar as value
    , value:modified::datetime as modified 
FROM bike_point_unnest1, 
LATERAL FLATTEN(
    additional_properties
    )
--LIMIT 10
;

SELECT *
FROM bike_point_unnest2;

---- Pivoting the flattened table ----


CREATE OR REPLACE TABLE bike_point_pivot AS
SELECT *
FROM bike_point_unnest2
PIVOT (
  MAX(value) FOR key IN ('NbStandardBikes', 'Locked', 'Installed', 'NbDocks', 'InstallDate', 'RemovalDate', 'NbBikes', 'TerminalName', 'Temporary', 'NbEmptyDocks', 'NbEBikes' )
  ) as p
      (
      id,
      modified_date,
      num_standard_bikes,
      locked,
      installed,
      num_docks,
      install_date,
      removal_date,
      num_bikes,
      terminal_name,
      temporary,
      num_empty_docks,
      num_e_bikes
      );
      
--- updating to correct data types and removing leading/trailing spaces and creating property table ----

CREATE OR REPLACE TABLE bike_point_properties AS 
SELECT
    TRIM(id) as id, 
    modified_date,
    TRIM(terminal_name) as terminal_name,
    CASE 
        WHEN installed ILIKE '%true%' THEN TRUE
        WHEN installed ILIKE '%false%' THEN FALSE
    END as installed,
    CASE 
        WHEN locked ILIKE '%true%' THEN TRUE
        WHEN locked ILIKE '%false%' THEN FALSE
    END as locked,
    TRIM(install_date) as install_date,
    TRIM(removal_date) as removal_date,
    CASE 
        WHEN temporary ILIKE '%true%' THEN TRUE
        WHEN temporary ILIKE '%false%' THEN FALSE
    END as temporary,
    num_bikes::INT as num_bikes,
    num_empty_docks::INT as num_empty_docks,
    num_docks::INT as num_docks,
    num_standard_bikes::INT as num_standard_bikes,
    num_e_bikes::INT as num_e_bikes
FROM bike_point_pivot;



--------- current_properties ------------
CREATE OR REPLACE TABLE bike_point_properties_current AS 
WITH MAX_DATE AS (
SELECT 
    MAX(modified_date) max_modified_date,
    id
FROM 
bike_point_properties
GROUP BY id
)


SELECT 
bp.*
FROM bike_point_properties as bp
INNER JOIN MAX_DATE as md ON md.id = bp.id AND md.max_modified_date = bp.modified_date 
;



----- Final tables ------
SELECT *
FROM bike_point_location;

SELECT *
FROM bike_point_properties;

SELECT *
FROM bike_point_properties_current;
