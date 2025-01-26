<h1>Module 1 Homework Solution</h1>

<h3> Question 1 </h3>
<p> **Code** : 
- sudo docker pull python:3.12.8
- sudo docker run -it 965ff0a5f344 /bin/bash
**Solution** : 
pip 24.3.1
</p>
<h2>Question2</h2>
<p>
**Solution**:
postgres:5432
</p>
<h3>Question 3</h3>
<p>
**SQL**:

```sql
SELECT
CASE
WHEN trip_distance <= 1 THEN 'Up to 1 mile'
WHEN trip_distance > 1 AND trip_distance <= 3 THEN 'In between 1 and 3 miles'
WHEN trip_distance > 3 AND trip_distance <= 7 THEN 'In between 3 and 7 miles'
WHEN trip_distance > 7 AND trip_distance <= 10 THEN 'In between 7 and 10 miles'
WHEN trip_distance > 10 THEN 'Over 10 miles'
END AS distance_category,
COUNT(*) AS trips_count
FROM
green_tripdata
WHERE
(lpep_dropoff_datetime >= '2019-10-01'  
AND lpep_dropoff_datetime < '2019-11-01')

GROUP BY
distance_category  
ORDER BY
distance_category;
```

**Solution**:
104,802; 198,924; 109,603; 27,678; 35,189
</p>

<h3> Question 4 </h3>
<p>
**SQL**:

```sql
SELECT max(trip_distance),lpep_pickup_datetime AS max_trip
FROM green_tripdata
group by lpep_pickup_datetime
order by max(trip_distance) desc;
```

**Solution**:
2019-10-31
</p>

<h3>Question 5 </h3>
<p>
**SQL**:

```sql
select tl."Zone", SUM(gt.total_amount) AS total_amount from green_tripdata gt inner join taxi_zone_lookup tl
on gt."PULocationID" = tl."LocationID"
WHERE
lpep_pickup_datetime >= '2019-10-18 00:00:00'
AND lpep_pickup_datetime < '2019-10-19 00:00:00'
group by tl."Zone"
having SUM(gt.total_amount)>13000;
```

**Solution**:
East Harlem North, East Harlem South, Morningside Heights
</p>

<h3> Question 6 </h3>
<p>
**SQL**:

```sql
SELECT
tl2."Zone" AS dropoff_zone,
MAX(gt.tip_amount) AS max_tip
FROM
green_tripdata gt
INNER JOIN
taxi_zone_lookup tl1 ON gt."PULocationID" = tl1."LocationID"
INNER JOIN
taxi_zone_lookup tl2 ON gt."DOLocationID" = tl2."LocationID"

gt.lpep_pickup_datetime >= '2019-10-01 00:00:00'
AND gt.lpep_pickup_datetime < '2019-11-01 00:00:00'
AND tl1."Zone" = 'East Harlem North'

GROUP BY
tl2."Zone"
ORDER BY
max_tip DESC
LIMIT 1;
```

**Solution**:
JFK Airport
</p>

<h3> Question 7 </h3>
<p>
**Solution**:
terraform import, terraform apply -y, terraform rm
</p>