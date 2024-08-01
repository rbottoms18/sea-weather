SELECT STRFTIME('%Y', Date) as Year, COUNT(IsRainyDay) as NumRainyDays
FROM SEA_rain
WHERE IsRainyDay = 1
GROUP BY Year