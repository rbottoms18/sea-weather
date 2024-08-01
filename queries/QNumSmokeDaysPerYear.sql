WITH NumSmokeDays AS (
        WITH TotalSmokeDays AS (
                SELECT DATE(DateTime) as Date
                FROM Sea_weather
                WHERE Condition='Smoke'
                GROUP BY Date
        )
        SELECT STRFTIME('%Y', Date) as Year, COUNT(Date) as NumDays
        FROM TotalSmokeDays
        GROUP BY STRFTIME('%Y', Date)
),
Years AS (
        SELECT DISTINCT STRFTIME('%Y', Sea_weather.DateTime) as Year
        FROM SEA_weather
)
SELECT Years.Year, IFNULL(NumSmokeDays.NumDays, 0) as NumDays
FROM Years
LEFT OUTER JOIN NumSmokeDays ON Years.Year = NumSmokeDays.Year
