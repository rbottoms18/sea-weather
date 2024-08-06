With MaxTempTimes AS (
        WITH RankedTemp AS (
            SELECT DATE(DateTime) as Date, TIME(DateTime) as Time, 
                Temperature, RANK() OVER (PARTITION BY DATE(DateTime) ORDER BY Temperature DESC) as Rank
            FROM SEA_weather
        )
        SELECT Date, TIME(AVG((STRFTIME('%H', Time) * 60 + STRFTIME('%M', Time)) * 60), 'unixepoch') AS AvgTime
        FROM RankedTemp
        WHERE Rank = 1
        GROUP BY Date
)
SELECT CAST(COUNT(Date) as DOUBLE) / (SELECT COUNT(*) FROM MaxTempTimes) as Freq, CAST(STRFTIME('%H', AvgTime) AS INT) as Hour
FROM MaxTempTimes
GROUP BY Hour