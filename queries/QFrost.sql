SELECT DATE(DateTime) as Date, "Dew Point", Temperature, Humidity
FROM SEA_weather
WHERE "Dew Point" = Temperature
AND Temperature <= 32
AND Temperature != 0
GROUP BY Date