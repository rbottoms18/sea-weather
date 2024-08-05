WITH CloudyDays AS (
    WITH CloudyEntries AS (
        SELECT Condition, CAST(STRFTIME('%H', DateTime) AS INT) as Hour, DATE(DateTime) as Date
        FROM Sea_weather
        WHERE Hour >= 6 AND Hour <= 20 AND Condition NOT IN ('Showers in the Vicinity', 'None', 'Mist', 'Thunder in the Vicinity', 
            'Smoke', 'Shallow Fog', 'Patches of Fog', 'Fog', 'Haze', 'Fair', 'Fair / Windy', 'Partly Cloudy / Windy', 'Partly Cloudy')
    )
    SELECT Date, STRFTIME('%Y', Date) as Year
    FROM CloudyEntries
    GROUP BY Date
    HAVING COUNT(DISTINCT(Hour)) >= 12
)
SELECT Year, CAST(COUNT(Date)AS DOUBLE) / 365 * 100  as PercentCloudy
FROM CloudyDays
GROUP BY Year