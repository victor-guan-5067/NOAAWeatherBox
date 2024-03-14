from typing import Literal
import Categories
import os
from datetime import date


def find_year_avg(months: list, temp: bool, decPlaces: Literal[0, 1, 2]) :
    divideBy = 12 if temp else 1
    
    total = 0

    match decPlaces:
        case 0:
            year_avg_str = '{}'
        case 1:
            year_avg_str = '{:.1f}'
        case 2:
            year_avg_str = '{:.2f}'

    for i in range(len(months)):
        month = float(months[i])
        total += month
    
    year_avg = year_avg_str.format(total/divideBy)
    return year_avg


def makeTable(file_path, location, state):
    months = Categories.months
    categories = {2:'precipitation inch', 3:'snow inch', 4:'mean F', 5:'high F', 6:'low F'}

    header = Categories.header.format(location, state)
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
            month_data = month_data.replace('\n', '')

            category = categories[i]

            match category:
                case 'precipitation inch':
                    precips.append(month_data)
                    precip += " | {} {} = {}\n".format(month, category, month_data)
                case 'snow inch':
                    snows.append(month_data)
                    snow += " | {} {} = {}\n".format(month, category, month_data)
                case 'mean F':
                    means.append(month_data)
                    mean_temp += " | {} {} = {}\n".format(month, category, month_data)
                case 'high F':
                    highs.append(month_data)
                    high_temp += " | {} {} = {}\n".format(month, category, month_data)
                case 'low F':
                    lows.append(month_data)
                    low_temp += " | {} {} = {}\n".format(month, category, month_data)
        
    climate_data.close()

    high_temp += " | year high F = {}\n".format(find_year_avg(highs, True, 1))
    mean_temp += " | year mean F = {}\n".format(find_year_avg(means, True, 1))
    low_temp += " | year low F = {}\n".format(find_year_avg(lows, True, 1))
    precip += " | year precipitation inch = {}\n".format(find_year_avg(precips, False, 2))

    if snow != "":
        snow += " | year snow inch = {}\n".format(find_year_avg(snows, False, 1))

    weatherBox = header + Categories.record_highs + high_temp + mean_temp + low_temp + Categories.record_lows + precip + Categories.precip_days
    if snow != "":
        weatherBox += snow + Categories.snow_days
    weatherBox += footer

    if state == "":
        path = f'{location}.txt'
    else:
        path = f'{state}/{location}.txt'

    parent_dir = os.getcwd()

    if not os.path.exists(f'{parent_dir}/{state}'):
        os.makedirs(f'{parent_dir}/{state}')
    
    with open(path, "w") as weatherBoxes:
        print(weatherBox, file=weatherBoxes)


if __name__ == '__main__':
    filePath = input("File path: ")
    location = input("Location: ")
    state = input("State: ")
    makeTable(filePath, location, state)

