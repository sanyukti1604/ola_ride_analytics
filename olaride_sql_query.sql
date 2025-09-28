-- 1. Retrieve all successful bookings:
select * from ola_dataset 
where Booking_Status = 'Success';

-- 2. Find the average ride distance for each vehicle type:
select avg(ride_distance) as avg_ride_distance, Vehicle_Type
from ola_dataset
group by Vehicle_Type;

-- 3. Get the total number of cancelled rides by customers:
SELECT SUM(Canceled_Rides_by_Customer) AS total_cancelled_by_customers
FROM ola_dataset;

-- 4. List the top 5 customers who booked the highest number of rides:
select customer_ID,count(Booking_ID) as total_ride from ola_dataset 
group by  customer_ID  
order by total_ride  DESC 
limit 5;

-- 5. Get the number of rides cancelled by drivers due to personal and car-related issues:
SELECT Incomplete_Rides_Reason, 
       COUNT(Canceled_Rides_by_Driver) AS total_cancelled_by_driver
FROM ola_dataset
WHERE Incomplete_Rides_Reason in ('Vehicle Breakdown','Customer Demand')
GROUP BY Incomplete_Rides_Reason;

-- 6  Find the maximum and minimum driver ratings for Prime Sedan bookings:
SELECT Vehicle_Type , MAX(CAST(Driver_Ratings AS DECIMAL(3,1))) AS max_driver_rating,
       MIN(CAST(Driver_Ratings AS DECIMAL(3,1))) AS min_driver_rating
FROM ola_dataset
WHERE Vehicle_Type = 'Prime Sedan';

-- 7. Retrieve all rides where payment was made using UPI:
SELECT COUNT(*) AS total_upi_rides
FROM ola_dataset
WHERE Payment_Method = 'UPI';

-- 8. Find the average customer rating per vehicle type:
select Vehicle_Type, avg(Customer_Rating) as avg_Customer_Rating 
from ola_dataset    
group by Vehicle_Type;

-- 9. Calculate the total booking value of rides completed successfully:
select sum(Booking_Value) as Total_Booking_Value,Booking_Status
from ola_dataset   
where Booking_Status = 'Success';

-- 10. List all incomplete rides along with the reason
SELECT Incomplete_Rides, Incomplete_Rides_Reason
FROM ola_dataset
WHERE Incomplete_Rides = 'Yes';
