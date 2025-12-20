-- 1. Top 10 strongest earthquakes (by magnitude)
SELECT id, country, mag
FROM earthquakes
ORDER BY mag DESC
LIMIT 10;


-- 2. Top 10 deepest earthquakes
SELECT id, country, depth_km
FROM earthquakes
ORDER BY depth_km DESC
LIMIT 10;


-- 3. Shallow earthquakes (< 50 km) with magnitude > 7.5
SELECT id, country, mag, depth_km
FROM earthquakes
WHERE depth_km < 50
  AND mag > 7.5;


-- 4. Average depth of earthquakes per country
SELECT country, AVG(depth_km) AS avg_depth
FROM earthquakes
GROUP BY country
ORDER BY avg_depth DESC;


-- 5. Average magnitude per magnitude type
SELECT magType, AVG(mag) AS avg_magnitude
FROM earthquakes
GROUP BY magType
ORDER BY avg_magnitude DESC;


-- 6. Year with the highest number of earthquakes
SELECT year, COUNT(*) AS total_earthquakes
FROM earthquakes
GROUP BY year
ORDER BY total_earthquakes DESC;


-- 7. Month with the highest number of earthquakes
SELECT month, COUNT(*) AS total
FROM earthquakes
GROUP BY month
ORDER BY total DESC;


-- 8. Day of the week with the most earthquakes
SELECT day_of_week, COUNT(*) AS total
FROM earthquakes
GROUP BY day_of_week
ORDER BY total DESC;


-- 9. Count of earthquakes per hour of the day
SELECT HOUR(time) AS hour_of_day, COUNT(*) AS total
FROM earthquakes
GROUP BY hour_of_day
ORDER BY hour_of_day;


-- 10. Most active reporting network
SELECT net, COUNT(*) AS total
FROM earthquakes
GROUP BY net
ORDER BY total DESC;


-- 11. Count of reviewed vs automatic earthquakes
SELECT status, COUNT(*) AS total
FROM earthquakes
GROUP BY status;


-- 12. Count of earthquakes by event type
SELECT type, COUNT(*) AS total
FROM earthquakes
GROUP BY type;


-- 13. Number of earthquakes by data types
SELECT types, COUNT(*) AS total
FROM earthquakes
GROUP BY types;


-- 14. Average RMS and GAP values per country (data quality)
SELECT country,
       AVG(rms) AS avg_rms,
       AVG(gap) AS avg_gap
FROM earthquakes
GROUP BY country;


-- 15. Events with high station coverage (nst > 50)
SELECT id, country, nst
FROM earthquakes
WHERE nst > 50
ORDER BY nst DESC;


-- 16. Number of tsunami-triggering earthquakes per year
SELECT year, COUNT(*) AS tsunami_events
FROM earthquakes
WHERE tsunami = 1
GROUP BY year
ORDER BY year;


-- 17. Average magnitude comparison: tsunami vs non-tsunami earthquakes
SELECT tsunami, AVG(mag) AS avg_magnitude
FROM earthquakes
GROUP BY tsunami;


-- 18. Top 5 countries with highest average earthquake magnitude
SELECT country, AVG(mag) AS avg_mag
FROM earthquakes
GROUP BY country
ORDER BY avg_mag DESC
LIMIT 5;


-- 19. Countries that experienced both shallow and deep earthquakes in the same month
SELECT DISTINCT e1.country, e1.year, e1.month
FROM earthquakes e1
JOIN earthquakes e2
  ON e1.country = e2.country
 AND e1.year = e2.year
 AND e1.month = e2.month
WHERE e1.depth_category = 'Shallow'
  AND e2.depth_category = 'Deep';


-- 20. Year-over-year growth in the number of earthquakes
SELECT year,
       COUNT(*) AS total,
       COUNT(*) - LAG(COUNT(*)) OVER (ORDER BY year) AS yoy_change
FROM earthquakes
GROUP BY year;


-- 21. Top 3 most seismically active regions
-- (based on frequency and average magnitude)
SELECT country,
       COUNT(*) AS frequency,
       AVG(mag) AS avg_magnitude
FROM earthquakes
GROUP BY country
ORDER BY frequency DESC, avg_magnitude DESC
LIMIT 3;


-- 22. Average depth of earthquakes near the equator (±5° latitude)
SELECT country, AVG(depth_km) AS avg_depth
FROM earthquakes
WHERE latitude BETWEEN -5 AND 5
GROUP BY country;


-- 23. Ratio of shallow to deep earthquakes by country
SELECT country,
       SUM(depth_category = 'Shallow') /
       NULLIF(SUM(depth_category = 'Deep'), 0) AS shallow_deep_ratio
FROM earthquakes
GROUP BY country;


-- 24. Events with the lowest data reliability
-- (high RMS and GAP values)
SELECT id, country, rms, gap
FROM earthquakes
ORDER BY rms DESC, gap DESC
LIMIT 10;


-- 25. Regions with the highest number of deep-focus earthquakes (>300 km)
SELECT country, COUNT(*) AS deep_quakes
FROM earthquakes
WHERE depth_km > 300
GROUP BY country
ORDER BY deep_quakes DESC;


-- 26. Earthquake count per country per year
SELECT country, year, COUNT(*) AS total
FROM earthquakes
GROUP BY country, year;


-- 27. Average magnitude by depth category
SELECT depth_category, AVG(mag) AS avg_magnitude
FROM earthquakes
GROUP BY depth_category;


-- 28. High significance earthquakes (sig > 800)
SELECT id, country, mag, sig
FROM earthquakes
WHERE sig > 800
ORDER BY sig DESC;


-- 29. Consecutive earthquakes within 1 hour
SELECT e1.id AS quake1, e2.id AS quake2,
       ABS(TIMESTAMPDIFF(MINUTE, e1.time, e2.time)) AS time_diff_minutes
FROM earthquakes e1
JOIN earthquakes e2
  ON e1.id <> e2.id
WHERE ABS(TIMESTAMPDIFF(MINUTE, e1.time, e2.time)) <= 60;


-- 30. Countries with frequent strong earthquakes (mag ≥ 6)
SELECT country, COUNT(*) AS strong_quakes
FROM earthquakes
WHERE mag >= 6
GROUP BY country
ORDER BY strong_quakes DESC;
