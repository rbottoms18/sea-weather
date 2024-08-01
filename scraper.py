"""
Ronan Bottoms
July 23, 2024

This file contains a simple web scraper to collect weather data from wunderground's KSEA station for a
user-inputed duration of years. The data is stored in memory in a pandas DataFrame before being saved to disk
in the local director both in CSV and .db (sqlite) format with the name 'SEA_weather'. Temporary backup files are saved
per completed year with the name '[YEAR]_SEA_weather.csv'.
"""

import os
from calendar import monthrange
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import threading
import time
import tqdm
from sqlalchemy import create_engine

cols = ["DateTime", "Temperature", "DewPoint", "Humidity", "Wind", "WindSpeed", "WindGust", "Pressure", "Precip", "Condition"]
months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]

# Selenium driver options
firefox_options = webdriver.FirefoxOptions()
firefox_options.add_argument("--headless")

def main():
    sea_weather = pd.DataFrame(columns=cols)
    
    # Get start year
    while(True):
        try: 
            start_year = int(input("Enter start year: "))
            while (start_year > 2024):
                print("Please enter a start year less than or equal to the current year.")
                start_year = int(input("Enter start year: "))
            break
        except: 
            print("Please enter an integer.")

    # Get end year
    while(True):
        try:
            end_year = int(input("Enter end year: "))
            while (end_year < start_year):
                print("Please enter an end year greater than or equal to the starting year.")
                end_year = int(input("Enter end year: "))
            while (int(end_year) > 2024):
                print("Please enter an end year less than or equal to the current year.")
                end_year = int(input("Enter end year: "))
            break
        except:
            print("Please enter an integer.")

    # Begin getting weather
    for year in range(start_year, end_year + 1):
        os.system("cls")
        print("Getting SEA weather for " + str(year) + ".")

        # Spawn four threads to work simultaneously
        # Tried using 12 threads, one for each month, but found no empirical speed up beyond 2-4.

        # Could also experiment with keeping the threads continuous over multiple years instead of ending them,
        # but that runs the risk of losing more data in the case of a crash. Safer to back up each year.
        
        threads = []
        num_threads = 4
        results = [pd.DataFrame(columns=cols)] * 12
        status = [1] * 12
        
        for i in range(0, num_threads):
            # Assign each thread a three-month sequential block
            threads.append(threading.Thread(target=get_months, args=(year, [3 * i + 1, 3 * i + 2, 3 * i + 3], results, status,)))
            threads[i].start()

        # Initiate progress bar
        display_thread = threading.Thread(target=display_status, args=(year, status,))
        display_thread.start()
        
        # Join threads together once all completed
        for i in range(0, num_threads):
            threads[i].join()

        # Concat and save results
        df = pd.DataFrame(columns=cols)
        df = pd.concat(results, ignore_index=True)

        # Save intermediate work in case of crash
        df.to_csv(str(year) + "_SEA_weather.csv")

        # Concat to total (doesn't take up much in memory so fine to keep here)
        sea_weather = pd.concat([sea_weather, df], ignore_index=True)
    
    # Save total as csv
    sea_weather.to_csv("SEA_weather.csv", index = False)
    
    # Save as sqlite db
    engine = create_engine('sqlite:///SEA_weather.db', echo=False)
    weather_sql = sea_weather.to_sql("weather", con=engine)


def get_months(year, months, results, status):
    """
    Get the weather data for a given set of months.

    Parameters
    ----------------
    year: int
        Year of the data to collect.
    months: list[int]
        Months this function collects data from.
    results: list[pd.DataFrame]
        Shared list of weather data in DataFrames indexed by month (start index 0).
    status: list[int]
        Shared list of current day in each month being scraped (start index 0).
    """
    for month in months:
        df = pd.DataFrame(columns=cols)
        with webdriver.Firefox(options=firefox_options) as driver:
            for day in range(1, monthrange(year, month)[1] + 1):
                status[month - 1] = day
                success = False
                while(not success):
                    try:
                        day_data = get_day(driver, year, month, day)
                        success = True
                    except:
                        print("Exception occured for " + str(year) + "-" + str(month) + "-" + str(day) + ". Retrying.")
                df = pd.concat([df, day_data], ignore_index=True)
            driver.close()
        # Save dataframe in the results
        results[month - 1] = df
        
    
def get_day(driver, year, month, day) -> pd.DataFrame:
    """
    Gets the weather data for a given day.

    Parameters
    ----------------
    driver: selenium.webdriver.Firefox
        Web driver to access the internet.
    year: int
        Year of the data to collect.
    month: int
        Month of the data to collect.
    day: int
        Day of the data to collect.

    Returns
    ----------------
    A pd.DataFrame containing weather data for the given day.
    """

    date = str(year) + "-" + str(month) + "-" + str(day)
    df = pd.DataFrame(columns=cols)

    # TODO: User-input weather station to collect data from.
    # EDIT HERE to change which station to scrape from. May need to alter the global cols variable
    # or get column names from the first row in the data table on the site.
    driver.get("https://www.wunderground.com/history/daily/us/wa/seattle/KSEA/date/" + date)

    # Attempt to get table data from the site
    results = []
    for i in range(0, 10):
        results = driver.find_elements(By.XPATH, '//tbody[@role="rowgroup"]')
        if (len(results) != 0): break
        time.sleep(1)
    
    # If no table was found after 10 tries, return as empty dataframe.
    if (len(results) == 0):
        return
    
    # By here table exists
    rows = results[0].find_elements(By.XPATH, '//tr[@class="mat-row cdk-row ng-star-inserted"]')

    # Extract information from each row
    for row in rows:
        cells = row.find_elements(By.XPATH, './*')
        row_data = [cells[i].text for i in range(0, len(cells))]

        # Append date to the time column
        row_data[0] = date + " " + row_data[0]

        # Remove units from numeric columns
        for i in [1, 2, 3, 5, 6, 7, 8]:
            row_data[i] = row_data[i].split(" ")[0]

        # Add row to dataframe
        df = pd.concat([df, pd.DataFrame([row_data], columns=cols)], ignore_index=True)
    
    # Cast first column to datetime
    df.loc[:, "Time"] = pd.to_datetime(df.loc[:, "Time"], format="%Y-%m-%d %I:%M %p")
    
    return df


def display_status(year, status):
    """
    Displays a progress bar for each month detailing the day being currently processed.

    Parameters
    ----------------
    year: int
        Year of the data being processed.
    status: list[int]
        Shared list of current day in each month being scraped (start index 0).
    """
    days_in_month = [monthrange(year, i + 1)[1] for i in range(0, 12)]
    pbars = [None] * 12
    for i in range(0, 12):
        pbars[i] = tqdm.tqdm(total=days_in_month[i], position=i)
        pbars[i].set_description(months[i])
    
    while (status != days_in_month):
        for i in range(0, 12):
            pbars[i].n = status[i]
            pbars[i].refresh()
        time.sleep(1)


if __name__ == "__main__":
    main()