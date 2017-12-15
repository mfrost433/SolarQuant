import mysql.connector
import os
import json
import datetime
from optparse import OptionParser
import argparse
import traceback as tb
import numpy as np
from DataRetriever import DataRetriever

dir = os.path.dirname(__file__)

argParser = argparse.ArgumentParser()
argParser.add_argument("-r", "--reqid", dest="reqId", help="ID for request",
                  metavar = "ID", required = True)


argParser.add_argument("-s", "--startdate", dest="startDate", help="start date",
                  metavar = "start")

argParser.add_argument("-e", "--enddate", dest="endDate", help="end date",
                  metavar = "end")

args = argParser.parse_args()

cnx = mysql.connector.connect(user='solarquant', password='solarquant',
                              host='localhost',
                              database='solarquant')
cursor = cnx.cursor()


#
#
#
#FOR FUTURE - FILL EMPTY VALUES IN WITH 00000000
#
#
#

def errorState():
    query = ("UPDATE training_requests SET STATUS = 5 "
             "WHERE REQUEST_ID = " + args.reqId)
    print(query)
    cursor.execute(query)
    cnx.commit()
    exit(1)


def logError(messg):
    f = "../logs/data_retrieval.txt"
    filename = os.path.join(dir, f)
    with open(filename, "a") as myfile:
        myfile.write("\nERROR:"+messg)

def getWeatherValue(word):
    weatherWords = [ "Fine","Partly cloudy","Cloudy", "Few showers", "Showers","Drizzle", "Windy","Fog", "Rain","Hail", "Thunder"]
    for i in range(len(weatherWords)):
        if(weatherWords[i] == word):
            return float(i)/(len(weatherWords)-1)


def populate():

    chunksFolder = os.path.join(dir, "chunks/")
    weatherFolder = os.path.join(dir, "weather/")
    #print(chunksFolder)
    for the_file in os.listdir(chunksFolder):
        file_path = os.path.join(chunksFolder, the_file)
        try:
            if os.path.isfile(file_path):
                1
                os.unlink(file_path)
        except Exception as e:
            print(e)


    for the_file in os.listdir(weatherFolder):
        file_path = os.path.join(weatherFolder, the_file)
        try:
            if os.path.isfile(file_path):
                1
                os.unlink(file_path)

        except Exception as e:
            print(e)

    startDate = args.startDate
    endDate = args.endDate


    infoQuery = "SELECT NODE_ID, SOURCE_ID FROM training_requests WHERE REQUEST_ID = "+args.reqId

    cursor.execute(infoQuery)
    data = cursor.fetchall()
    for row in data:
        nodeId = str(row[0])
        srcId = str(row[1])


    try:
        1
        dr = DataRetriever(nodeId, srcId, startDate, endDate)
        dr.getNodeData()
        dr.getWeatherData()
    except Exception as e:
        tb.print_exc(e)
        logError(str(e))
        errorState()

    startDateDt = dr.startDate
    endDateDt = dr.endDate
    resultSet = []

    for fname in sorted(os.listdir(chunksFolder)):
        dataFile = open(chunksFolder + fname, 'r').read()
        resultSet.append(json.loads(dataFile))

    resultWeatherSet = []
    for fname in sorted(os.listdir(weatherFolder)):
        dataFile = open(weatherFolder + fname, 'r').read()
        resultWeatherSet.append(json.loads(dataFile))


    query2 = ("INSERT INTO weather_data VALUES (%s, %s, %s, %s, %s)")
    dat = []

    for i in resultWeatherSet:
        dataTemp = []
        try:
            for j in i['data']['results']:
                cDate = datetime.datetime.strptime(j['created'], "%Y-%m-%d %H:%M:%S.%fZ")

                if (cDate > startDateDt):
                    dataTemp = [(cDate,j['sky'], j['temp'], j['humidity'],j['atm']) ]
                    dat = dat + dataTemp
        except Exception as e:
            1

            logError(str(e))

    try:
        cursor.executemany(query2, dat)
    except Exception as e:
        logError(str(e))

    cnx.commit()

    query2 = ("INSERT INTO node_datum VALUES (%s, %s, %s, %s)")

    prevDate = datetime.datetime.strptime("1000","%Y")
    dat = []
    for i in resultSet:
        dataTemp = []
        try:
            for j in i['data']['results']:
                cDate = datetime.datetime.strptime(j['created'],"%Y-%m-%d %H:%M:%S.%fZ")
                if ((cDate > startDateDt) & (prevDate < cDate)):

                    dataTemp = [(nodeId, srcId, cDate, j['wattHours'])]

                    dat = dat+dataTemp
                    prevDate = cDate
        except Exception as e:
            logError(str(e))
    try:
        cursor.executemany(query2, dat)
    except Exception as e:
        logError(str(e))
        tb.print_exc(e)


    cnx.commit()
    data = []
    weatherData = []
    for j in range(2):
        for i in range(7):
            i = i+1
            min = j*30
            queryData = "SELECT DATE_CREATED, WATT_HOURS FROM node_datum WHERE NODE_ID = " + nodeId + " AND SOURCE_ID = '" + srcId+ \
                        "' AND MINUTE(DATE_CREATED) = " + str(min)+" AND DAYOFWEEK(DATE_CREATED) = " + str(i) + \
                        " ORDER BY HOUR(DATE_CREATED), DATE_CREATED desc"
            try:
                cursor.execute(queryData)
                data = data+cursor.fetchall()
            except Exception as e:
                logError(str(e))


    input = []
    j = 0
    def getWeatherForDate(date):
     	queryWeather = "SELECT DATE_CREATED, TEMP, HUMIDITY, ATM FROM weather_data WHERE DATE_CREATED = '" + str(date)+"'"

        cursor.execute(queryWeather)
        dataW = cursor.fetchall()
        return dataW

    count = 0
    trainingStart = datetime.datetime.utcnow() - datetime.timedelta(weeks=24)
    for i in range(len(data) - 2):
        if(data[i][0] > trainingStart):
            if(data[i+1][0] == data[i][0] - datetime.timedelta(days=7)):
                if (data[i + 2][0] == data[i][0] - datetime.timedelta(days=14)):

                    weatherData = getWeatherForDate(data[i][0])

                    try:
                        weatherVal = getWeatherValue(weatherData[0][2])
                        if(weatherVal == None):
                            1
                        input = input + [(nodeId,srcId,data[i][0], datetime.datetime.utcnow(),
                        data[i][1],data[i+1][1],data[i+2][1],weatherData[0][3],weatherData[0][2],weatherData[0][1])]

                    except Exception as e:
                        count+=1

    query4 = ("INSERT INTO training_input "
             "VALUES (%s,%s,%s, %s, %s, %s, %s, %s, %s,%s)")
    try:
        cursor.executemany(query4,input)
    except Exception as e:
        logError(str(e))
        tb.print_exc(e)

    cnx.commit()
    for the_file in os.listdir(chunksFolder):
        file_path = os.path.join(chunksFolder, the_file)
        try:
            if os.path.isfile(file_path):
                1
                os.unlink(file_path)
        except Exception as e:
            logError(str(e))

    for the_file in os.listdir(weatherFolder):
        file_path = os.path.join(weatherFolder, the_file)

        try:
            if os.path.isfile(file_path):
                1
                os.unlink(file_path)
        except Exception as e:
            logError(str(e))

try:
    populate()
except Exception as e:
    logError(str(e))
    tb.print_exc(e)
    errorState()
