WITH RankedTemp AS (
        SELECT DATE(DateTime) as Date, TIME(DateTime) as Time, Temperature, RANK() OVER (PARTITION BY DATE(DateTime) ORDER BY Temperature DESC) as Rank
        FROM SEA_weather
)
SELECT Date, TIME(AVG((STRFTIME('%H', Time) * 60 + STRFTIME('%M', Time)) * 60), 'unixepoch') AS AvgTime, Temperature
FROM RankedTemp
WHERE Rank = 1
GROUP BY Date