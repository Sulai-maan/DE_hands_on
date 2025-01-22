# Solutions to Datatalks DE Bootcamp Weekly Assignments

# Week 1

## Question 1. Understanding docker first run

```bash
docker run --rm -it --entrypoint bash python:3.12.8
```
Then, at the tty, run:

```bash
pip --version
```

## Question 3. Trip Segmentation Count

### Up to 1 mile
```sql
WITH up_to_one_mile AS (
        SELECT * FROM green_taxi_trips WHERE trip_distance <= 1::real
        )
        SELECT COUNT(*) FROM up_to_one_mile WHERE
        lpep_pickup_datetime >= '2019-10-01' AND lpep_dropoff_datetime < '2019-11-01';
```

### In between 1 (exclusive) and 3 miles (inclusive)
```sql
WITH three_miles AS (
        SELECT * FROM green_taxi_trips WHERE trip_distance > 1::real AND trip_distance <= 3::real
        )
        SELECT COUNT(*) FROM three_miles WHERE
        lpep_pickup_datetime >= '2019-10-01' AND lpep_dropoff_datetime < '2019-11-01'
```
### In between 3 (exclusive) and 7 miles (inclusive)
```sql
WITH three_to_seven_miles AS (
        SELECT * FROM green_taxi_trips WHERE trip_distance > 3::real AND trip_distance <= 7::real
        )
        SELECT COUNT(*) FROM three_to_seven_miles WHERE
        lpep_pickup_datetime >= '2019-10-01' AND lpep_dropoff_datetime < '2019-11-01';
```

### In between 7 (exclusive) and 10 miles (inclusive)
```sql
WITH seven_to_ten_miles AS (
        SELECT * FROM green_taxi_trips WHERE trip_distance > 7::real AND trip_distance <= 10::real
        )
        SELECT COUNT(*) FROM seven_to_ten_miles WHERE
        lpep_pickup_datetime >= '2019-10-01' AND lpep_dropoff_datetime < '2019-11-01';
```
### Over 10 miles
```sql
WITH over_ten_miles AS (
        SELECT * FROM green_taxi_trips WHERE trip_distance > 10::real
        )
        SELECT COUNT(*) FROM over_ten_miles WHERE
        lpep_pickup_datetime >= '2019-10-01' AND lpep_dropoff_datetime < '2019-11-01';
```

## Question 4. Longest trip for each day
```sql
SELECT lpep_pickup_datetime, RANK() OVER (ORDER BY(trip_distance) DESC) as rank_by_distnace
FROM green_taxi_trips LIMIT 1; 
```

## Question 5. Three biggest pickup zones
```sql
WITH over_13000 AS (
        SELECT "PULocationID", SUM(total_amount) as sum_total
        FROM green_taxi_trips WHERE lpep_pickup_datetime::date = '2019-10-18'::date AND total_amount IS NOT NULL
        GROUP BY "PULocationID" HAVING SUM(total_amount) > 13000)

        SELECT *
        FROM over_13000 qt
        JOIN taxi_zones tz ON qt."PULocationID" = tz."LocationID"
        ORDER BY sum_total DESC
```

## Question 6. Largest tip
```sql
WITH zone_id AS (
	SELECT "LocationID"
	FROM taxi_zones
	WHERE "Zone" = 'East Harlem North' 
), top_tip AS (
    SELECT *
    FROM green_taxi_trips gtt
    JOIN zone_id zi on gtt."PULocationID" = zi."LocationID"
    ORDER BY tip_amount DESC LIMIT 1)

    SELECT "Zone"
    FROM taxi_zones tz 
    JOIN top_tip tt ON tz."LocationID" = tt."DOLocationID" 
```