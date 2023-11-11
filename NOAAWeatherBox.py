import csv, Categories
import re
import os
from datetime import date

def aggYear(months, temp, decPlaces) :
    divideBy = 12 if temp else 1
    
    total = 0
    places = ''
    if decPlaces == 1:
        places = '{:.1f}'
    elif decPlaces == 2:
        places = '{:.2f}'

    for i in range(len(months)):
        month = float(months[i])
        total += month
    
    year_avg = places.format(total/divideBy)
    return year_avg


def makeTable(file_path, location):
    months = Categories.month
    catNums = {2:'precipitation inch', 3:'snow inch', 4:'mean F', 5:'high F', 6:'low F'}

    header = Categories.header.format(location)
    precip = " | precipitation colour   = green\n"
    snow = ""
    high_temp = ""
    low_temp = ""
    mean_temp = ""
    date_string = date.today().strftime("%B %-d, %Y")
    footer = Categories.footer.format(date_string, date_string)

    precips = []
    snows = []
    highs = []
    lows = []
    means = []

    climate_data = open(file_path, newline='')
    climate_data.readline()

    for row in climate_data:
        split_row = row.split(",")
        month = months[split_row[1]]
        
        for i in range(2, len(split_row)):
            month_data = split_row[i].replace(' ','')
            month_data = month_data.replace('"','')
            month_data = month_data.replace('\n', "")

            cat = catNums[i]

            if (cat == 'precipitation inch'):
                precips.append(month_data)
                precip += " | {} {} = {}\n".format(month, cat, month_data)
            if (cat == 'snow inch' and month_data != ""):
                snows.append(month_data)
                snow += " | {} {} = {}\n".format(month, cat, month_data)
            if (cat == 'mean F'):
                means.append(month_data)
                mean_temp += " | {} {} = {}\n".format(month, cat, month_data)
            if (cat == 'high F'):
                highs.append(month_data)
                high_temp += " | {} {} = {}\n".format(month, cat, month_data)
            if (cat == 'low F'):
                lows.append(month_data)
                low_temp += " | {} {} = {}\n".format(month, cat, month_data)
        
    climate_data.close()

    year_precip = aggYear(precips, False, 2)
    year_snow = aggYear(snows, False, 1) if snow != "" else 0
    year_high = aggYear(highs, True, 1)
    year_low = aggYear(lows, True, 1)
    year_mean = aggYear(means, True, 1)

    precip += " | year precipitation inch = {}\n".format(year_precip)
    if snow != "":
        snow += " | year snow inch = {}\n".format(year_snow)
    high_temp += " | year high F = {}\n".format(year_high)
    low_temp += " | year low F = {}\n".format(year_low)
    mean_temp += " | year mean F = {}\n".format(year_mean)

    weatherBox = header + Categories.record_highs + high_temp + mean_temp + low_temp + Categories.record_lows + precip + Categories.precip_days
    if snow != "":
        weatherBox += snow + Categories.snow_days
    weatherBox += footer

    state_names = ["Alaska", "Alabama", "Arkansas", "American Samoa", "Arizona", "California", "Colorado", "Connecticut", "District ", "of Columbia", "Delaware", "Florida", "Georgia", "Guam", "Hawaii", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine", "Michigan", "Minnesota", "Missouri", "Mississippi", "Montana", "North Carolina", "North Dakota", "Nebraska", "New Hampshire", "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Puerto Rico", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Virginia", "Virgin Islands", "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"]

    path_state = ''
    for state in state_names:
        if ", " + state in location: 
            path_state = state

    path = '/Users/victorguan/Documents/WeatherBoxes/NOAA/{}/{}.txt'.format(path_state, location)     
    
    with open(path, "w") as weatherBoxes:
        print(weatherBox, file=weatherBoxes)

if __name__ == '__main__':
    filePath = input("File path: ")
    location = input("location: ")
    makeTable(filePath, location)

