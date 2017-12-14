from urllib2 import Request, urlopen, URLError
import xml.etree.ElementTree as xmlParse
import traceback as tb
import datetime as dt
import os
import mysql.connector
import datetime
import json
from DataRetriever import DataRetriever



directory = os.path.dirname(__file__)
weatherFolder = os.path.join(directory, "weather/")
weatherFile = weatherFolder + '/weather_future.xml'

cnx = mysql.connector.connect(user='solarquant', password='solarquant',
                              host='localhost',
                              database='solarquant')
PREFIX = "https://data.solarnetwork.net"

chunksFolder = os.path.join(directory, "chunks/")
cursor = cnx.cursor()




def updateWeather():

    #fills in all 30 minute intervals with data.
    def interpolate(data):
        out = []
        for i in range(len(data)-1) :
            diff = data[i+1][0] - data[i][0]
            mins = divmod(diff.total_seconds(),60*30)

            for j in range(int(mins[0])):
                out.append([data[i][0]  + datetime.timedelta(minutes=30*j)] + data[i][1:])
        return out

    def getWeatherData():

        request = Request("http://api.met.no/weatherapi/locationforecast/1.9/?lat=-36.855401;lon=174.745393")
        data = ""
        try:
            response = urlopen(request)
            data = xmlParse.parse(response)
            data.write(weatherFile)
        except Exception as e:
            print("Failed")
            1
            #tb.print_exc(e)

    dateFormat = "%Y-%m-%dT%H:%M:%SZ"

    def addToDatabase():
        xml = xmlParse.parse(weatherFile)
        root = xmlParse.parse(weatherFile).getroot()
        data = []
        for i in xml.iter(tag = "time"):
            tempArr = []
            toDate = dt.datetime.strptime(i.get("to"), dateFormat)
            fromDate = dt.datetime.strptime(i.get("from"), dateFormat)

            if( toDate == fromDate ):
                tempArr.append(toDate)
                for j in i:
                    try:
                        temp = float(j.find("temperature").get("value"))
                        windDir = float(j.find("windDirection").get("deg"))
                        windSpeed = float(j.find("windSpeed").get("mps"))
                        humidity = float(j.find("humidity").get("value"))
                        #hPa
                        pressure = float(j.find("pressure").get("value"))
                        cloudy = float(j.find("cloudiness").get("percent"))
                        tempArr = tempArr + [temp,windDir,windSpeed,humidity,pressure,cloudy]

                    except Exception as e:
                        1
                        #tb.print_exec(e)
            if(len(tempArr) > 4):
                data.append(tempArr)
        data = interpolate(data)
        cursor = cnx.cursor()
        query = "INSERT INTO yr_weather VALUES (%s, %s, %s, %s, %s, %s, %s)"
        try:
            cursor.executemany(query, data)
        except Exception as e:
            1
            #tb.print_exc(e)

        cnx.commit()
    getWeatherData()
    addToDatabase()


def updateDatum(nodeId, srcId, endDate=datetime.datetime.today(), startDate = datetime.datetime.today() - datetime.timedelta(days=14)):


    def getChunkEndDate( current, endDate, minInterval):
        out = current + datetime.timedelta(minutes=500 * minInterval)
        if (out > endDate):
            return endDate
        else:
            return out

    def getNodeData():

        chunkStart = startDate
        while (chunkStart < endDate):
            chunkEnd = getChunkEndDate(chunkStart, endDate, 20)

            startString = datetime.datetime.strftime(chunkStart, "%Y-%m-%dT12%%3A00")

            endString = datetime.datetime.strftime(chunkEnd, "%Y-%m-%dT12%%3A00")

            request = Request(PREFIX + "/solarquery/api/v1/pub/datum/"
                                            "list?nodeId=" + nodeId + "&aggregation=ThirtyMinute&startDate=" +
                              startString + "&endDate=" + endString + "&sourceIds=" + srcId + "&max=5000000")
            data = ""

            try:
                response = urlopen(request)
                data = json.loads(response.read())
                dat = []

                query = ("INSERT INTO node_datum VALUES (%s, %s, %s, %s)")


                prevDate = datetime.datetime.strptime("1000", "%Y")
                dat = []
                for i in data['data']['results']:
                    dataTemp = []
                    try:
                        cDate = datetime.datetime.strptime(i['created'], "%Y-%m-%d %H:%M:%S.%fZ")
                        if ((cDate > startDate) & (prevDate < cDate)):

                            dataTemp = [(nodeId, srcId, cDate, i['wattHours'])]
                            dat = dat + dataTemp
                            prevDate = cDate

                    except Exception as e:
                        1
                        #tb.print_exc(e)

                try:
                    cursor.executemany(query, dat)
                except Exception as e:
                    tb.print_exc(e)
            except Exception as e:
                print("Failed")

            chunkStart = chunkEnd

            cnx.commit()

    getNodeData()

def addPredictionInput(nodeId, srcId, endDate=datetime.datetime.today(), startDate = datetime.datetime.today() - datetime.timedelta(days=14)):
    data = []
    startDate = datetime.datetime.today() - datetime.timedelta(days=14)
    for j in range(2):
        for i in range(7):
            i = i + 1
            min = j * 30
            queryData = "SELECT DATE_CREATED, WATT_HOURS FROM node_datum WHERE NODE_ID = " + nodeId + " AND SOURCE_ID = '" + srcId + \
                        "' AND MINUTE(DATE_CREATED) = " + str(min) + " AND DAYOFWEEK(DATE_CREATED) = " + str(i) + \
                        " ORDER BY HOUR(DATE_CREATED), DATE_CREATED desc"
            try:
                cursor.execute(queryData)
                data = data + cursor.fetchall()
            except Exception as e:
                1
                #tb.print_exc(e)



    j = 0

    def getWeatherForDate(date):
     	queryWeather = "SELECT PREDICTION_DATE,TEMP,CLOUDINESS FROM yr_weather WHERE PREDICTION_DATE = '" + str(date)+"'"
        cursor.execute(queryWeather)
        dataW = cursor.fetchall()
        return dataW
    input = []
    count = 0
    #print(data)
    for i in range(len(data) - 2):
        if(data[i][0] > startDate):

            if(data[i+1][0] == data[i][0] - datetime.timedelta(days=7)):
                predictionDate = data[i][0] + datetime.timedelta(days=7)
                weatherData = getWeatherForDate(predictionDate)

                try:
                    input = input + [(nodeId,srcId,predictionDate, datetime.datetime.utcnow(),
                    data[i][1],data[i+1][1],weatherData[0][1],float(weatherData[0][2])/100)]

                except Exception as e:
                    #tb.print_exc(e)
                    count+=1
    query4 = ("INSERT INTO tensorflow_prediction_input "
             "VALUES (%s,%s,%s, %s, %s, %s, %s, %s)")
    try:
        cursor.executemany(query4,input)
    except Exception as e:
        1
        #tb.print_exc(e)
    cnx.commit()

