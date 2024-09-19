
-- unoptimized query; unnecessary to join location and department
SELECT Location.location_id
FROM Location
INNER JOIN Department
ON Department.location = Location.location_id
GROUP BY Location.location_id
ORDER BY COUNT(*)
LIMIT 1;

-- optimized query
SELECT location
FROM Department
GROUP BY location
ORDER BY COUNT(*)
LIMIT 1;

