# -*- coding: utf-8 -*-
# @Author: Hadrien Sattelmayer
# @Date:   2020-06-07 23:44:48
# @Last Modified by:   Hadrien Sattelmayer
# @Last Modified time: 2020-06-07 23:50:52

from datetime import datetime, timedelta, date
from functools import reduce
import requests
import numpy as np
import json

def main():
    wc = WeatherCalculator()
    
    #get json with weather infos
    weatherJson = wc.apiConnect()
    
    #get dict with days and weekday
    days= wc.getdayRange()

    #get dict with days and humidity
    weather_dict = wc.getHumidity(weatherJson)
    for key, value in weather_dict.items():
        print(key,value)

    #update dict days with weekdays name
    days_dict = wc.updateDayDict(days)

    #get list of weekdays names that the humidity is greater than 70
    rainyDays = wc.verifyRainyDays(weather_dict, days_dict)
    rainyDays = str(rainyDays)
    rainyDays = rainyDays.replace("[", " ")
    rainyDays = rainyDays.replace("]", " ")

    print("You should take an umbrella in these days: "+ rainyDays)



class WeatherCalculator:
    
    def __init__(self):
        self.city_id = "3451328"
        self.user_key = "390a8a5a2b010c465824a52c9827b1e6"
        self.week_days = {
            0 : "Monday",
            1 : "Tuesday",
            2 : "Wednesday",
            3 : "Thursday",
            4 : "Friday",
            5 : "Saturday",
            6 : "Sunday"
        }


        


    def apiConnect(self):
        """This function connect with the API

        Returns:
            [Json]: [Returns a json with the weather information for the next five days]
        """

        url = "http://api.openweathermap.org/data/2.5/forecast?id=%s&appid=%s" %(self.city_id, self.user_key)
        r = requests.get(url=url)

        weather = r.json()
        return weather



    def getHumidity(self, json):
        """This function creates a dict for each day and its humidity

        Args:
            json ([Json]): Json with the weather information for the next five days

        Returns:
            [dict]: dict with de humidity for each day
        """
        daysList, values_hum = [], []
        days = {}

        for weather_days in json["list"]:
            date = str(weather_days["dt_txt"])
            date = date.split(" ")[0]
            print(date, weather_days["main"]["humidity"])
            if date not in daysList:
                values_hum.clear()
                values_hum.append(weather_days["main"]["humidity"])
                daysList.append(date)
                days.update({date : weather_days["main"]["humidity"]})
            else:
                values_hum.append(weather_days["main"]["humidity"])
                value_mean = np.mean(values_hum)
                days.update({date : value_mean})
        return days


    def getdayRange(self):
        """This function creates a dict with the the days and its weekday number

        Returns:
            [dict]: Contains the the days and its weekday number
        """
        days = {}
        td = datetime.now()

        for i in range(5):
            date = td + timedelta(days=i+1)
            week_day = datetime.weekday(date)
            date = str(date).split(" ")[0]
            days.update({date : week_day})

        return days



    def updateDayDict(self, daysDict):
        """This function updates the daysDict changing the weekday number with weekday name

        Args:
            daysDict ([dict]): Contains the range of days and its weekdays number

        Returns:
            [dict]: Updated dict containing the range of days and its weekday name
        """

        for key, value in daysDict.items():
            daysDict.update({key : self.week_days[value]})

        return daysDict


    def verifyRainyDays(self, weather_dict, days_dict):
        """This function checks if the day's humidity is greater than 70
        Args:
            weather_dict ([type]): Dict with the day's weather infos
            days_dict ([type]): Dict with the days and its weekday names

        Returns:
            [list]: List with the days of the week that the humidity is greater than 70
        """
        rainyDays = []
        for key, value in weather_dict.items():
            if value >= 70:
                try:
                    rainyDays.append(days_dict[key])
                except:
                    pass
        
        return rainyDays


if __name__ == "__main__":
    main()