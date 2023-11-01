import csv, Categories
import re
from datetime import date

months = Categories.month

catNums = {2:'precip',3:'snow',4:'mid', 5:'high', 6:'low'}

def makeTable(file_path, location):
    header = Categories.header.format(location)
    precip = " | precipitation colour   = green\n"
    snow = ""
    high_temp = ""
    low_temp = ""
    mean_temp = ""
    today = date.today()
    date_string = today.strftime("%B %d, %Y")
    footer = Categories.footer.format(date_string, date_string)
    climate_data = open(file_path, newline='')
    climate_data.readline()

    for row in climate_data:
        split_row = row.split(",")
        month = months[split_row[1]]
        
        for i in range(2, len(split_row)):
            month_data = split_row[i].replace(' ','')
            month_data = month_data.replace('"','')
            month_data = month_data.replace('\n', "")
            if (catNums[i] == 'precip'):
                precip += (" | {} precipitation inch = {}\n".format(month, month_data))
            if (catNums[i] == 'snow' and month_data != ""):
                snow += (" | {} snow inch = {}\n".format(month, month_data))
            if (catNums[i] == 'mid'):
                mean_temp += (" | {} mean F = {}\n".format(month, month_data))
            if (catNums[i] == 'high'):
                high_temp += (" | {} high F = {}\n".format(month, month_data))
            if (catNums[i] == 'low'):
                low_temp += (" | {} low F = {}\n".format(month, month_data))
        
    climate_data.close()

    precip += " | year precipitation inch = \n"
    snow += " | year snow inch = \n"
    high_temp += " | year high F = \n"
    low_temp += " | year low F = \n"
    mean_temp += " | year mean F = \n"

    weatherBox = header + Categories.record_highs + high_temp + mean_temp + low_temp + Categories.record_lows + precip + Categories.precip_days
    if snow != "":
        weatherBox += snow + Categories.snow_days
    weatherBox += footer

    path = location + ".txt"
    with open(path, "a") as weatherBoxes:
        print(weatherBox, file=weatherBoxes)

if __name__ == '__main__':
    filePath = input("File path: ")
    location = input("location: ")
    makeTable(filePath, location)

