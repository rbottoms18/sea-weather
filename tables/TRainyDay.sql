CREATE TABLE SEA_rain AS WITH DailyPrecip_MM AS (
        SELECT DATE(DateTime) as Date, SUM(Precip * 25.4) as TotalPrecip_mm
        FROM SEA_weather
        GROUP BY Date
)
SELECT Date, TotalPrecip_mm, CASE
        WHEN TotalPrecip_mm = 0.0 THEN 'No Rain'
        WHEN TotalPrecip_mm >= 0.1 AND TotalPrecip_mm < 1.0 THEN 'Very Light Rain'
        WHEN TotalPrecip_mm >= 1.0 AND TotalPrecip_mm < 11.0 THEN 'Light Rain'
        WHEN TotalPrecip_mm >= 11.0 AND TotalPrecip_mm < 31.0 THEN 'Moderate Rain'
        WHEN TotalPrecip_mm >= 31.0 AND TotalPrecip_mm < 71.0 THEN 'Heavy Rain'
        WHEN TotalPrecip_mm >= 71.0 AND TotalPrecip_mm < 151.0 THEN 'Very Heavy Rain'
        WHEN TotalPrecip_mm >= 151.0 THEN 'Extremely Heavy Rain'
        ELSE 'NULL'
END AS RainIntensity,
CASE
        WHEN TotalPrecip_mm >= 1.0 THEN CAST(1 AS BIT)
        ELSE CAST(0 AS BIT)
END AS IsRainyDay
FROM DailyPrecip_MM
