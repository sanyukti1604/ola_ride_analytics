create database olaride_db;
use olaride_db;

select * from ola_dataset;

SELECT 
    COUNT(*) AS total_rows,
    SUM(CASE WHEN booking_id IS NULL THEN 1 ELSE 0 END) AS null_booking_id,
    SUM(CASE WHEN customer_id IS NULL THEN 1 ELSE 0 END) AS null_customer_id,
    SUM(CASE WHEN booking_status IS NULL THEN 1 ELSE 0 END) AS null_booking_status,
    SUM(CASE WHEN pickup_location IS NULL THEN 1 ELSE 0 END) AS null_pickup_location,
    SUM(CASE WHEN drop_location IS NULL THEN 1 ELSE 0 END) AS null_drop_location,
    SUM(CASE WHEN Canceled_Rides_by_Customer IS NULL THEN 1 ELSE 0 END) AS null_cancelled_by_customer,
    SUM(CASE WHEN Canceled_Rides_by_Driver IS NULL THEN 1 ELSE 0 END) AS null_cancelled_by_driver,
    SUM(CASE WHEN Driver_Ratings IS NULL THEN 1 ELSE 0 END) AS null_driver_rating,
    SUM(CASE WHEN Customer_Rating IS NULL THEN 1 ELSE 0 END) AS null_customer_rating
FROM ola_dataset;

UPDATE ola_dataset
SET Canceled_Rides_by_Customer = 0
WHERE Canceled_Rides_by_Customer IS NULL;

UPDATE ola_dataset
SET Canceled_Rides_by_Driver = 0
WHERE Canceled_Rides_by_Driver IS NULL;

-- Replace NULL ratings with 0
UPDATE ola_dataset
SET Driver_Ratings = 0
WHERE Driver_Ratings IS NULL; 

UPDATE ola_dataset
SET customer_rating = 0
WHERE customer_rating IS NULL;


