# About

In this short project I created a a web scraper using Python to scrape weather data from the [SeaTac Airport Wunderground Station](https://www.wunderground.com/weather/us/wa/seattle/KSEA). 
The scraper operates in a threaded manner and can pull data for a user-inputted range of years. It compiles and saves the data in `.csv` and `.sql` formats.

I then used SQL in Python via the `sqlite3` package to perform some basic analysis of the data, including determining the time of the maximum temperature for each day, 
how often Seattle is rainy or cloudy, and how often Seattle experiences smoke.

View `weather_exploration.ipynb` to see the full analysis.


<p align="center">
  <img src="https://github.com/rbottoms18/sea-weather/blob/master/img/max_temp_freq_summer.png"/>
</p>

<p align="center">
  <img src="https://github.com/rbottoms18/sea-weather/blob/master/img/seattle_rain_types.png"/>
</p>

<p align="center">
  <img src="https://github.com/rbottoms18/sea-weather/blob/master/img/cloudy_days_per_year.png"/>
</p>
