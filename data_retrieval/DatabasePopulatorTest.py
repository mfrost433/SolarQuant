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


def logError(messg):
    f = "../logs/data_retrieval.txt"
    filename = os.path.join(dir, f)
    with open(filename, "a") as myfile:
        myfile.write("\nERROR:"+messg)


def populate():


    chunksFolder = os.path.join(dir, "chunks/")
    weatherFolder = os.path.join(dir, "weather/")
    #print(chunksFolder)
    for the_file in os.listdir(chunksFolder):
        file_path = os.path.join(chunksFolder, the_file)
        try:
            if os.path.isfile(file_path):
                1
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)


    for the_file in os.listdir(weatherFolder):
        file_path = os.path.join(weatherFolder, the_file)
        try:
            if os.path.isfile(file_path):
                1                # elif os.path.isdir(file_path): shutil.rmtree(file_path)
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

    dr = DataRetriever(nodeId,srcId,startDate, endDate)
    try:
        1
        #dr.getNodeData()
        #dr.getWeatherData()
    except:
        errorState()


    resultSet = []
    for fname in sorted(os.listdir(chunksFolder)):
        dataFile = open(chunksFolder + fname, 'r').read()
        resultSet.append(json.loads(dataFile))

    resultWeatherSet = []
    for fname in sorted(os.listdir(weatherFolder)):
        dataFile = open(weatherFolder + fname, 'r').read()
        resultWeatherSet.append(json.loads(dataFile))

    query2 = ("INSERT INTO node_datum VALUES (%s, %s, %s, %s)")
    dat = []

    for i in resultSet:
        dataTemp = []
        try:
            dataTemp = [(nodeId, srcId, datetime.datetime.strptime(j['created'],"%Y-%m-%d %H:%M:%S.%fZ"),
              j['wattHours']) for j in i['data']['results']]

            dat = dat+dataTemp
        except Exception as e:
            1

    try:
        cursor.executemany(query2, dat)
    except:
        1

    cnx.commit()

    query3 = "SELECT DATE_CREATED, WATT_HOURS FROM node_datum ORDER BY YEAR(DATE_CREATED),HOUR(DATE_CREATED),DAYOFWEEK(DATE_CREATED),WEEKOFYEAR(DATE_CREATED) DESC"

    cursor.execute(query3)
    data = cursor.fetchall()
    input = []
    for i in range(len(data) - 2):
        print(data[i][0])
        print(data[i+1][0])
        print()
        if(data[i+1][0] == data[i][0] - datetime.timedelta(days=7)):
            if (data[i + 2][0] == data[i][0] - datetime.timedelta(days=14)):
                input = input + [(nodeId,srcId,data[i][0], datetime.datetime.today(),
                 data[i][1],data[i+1][1],data[i+2][1])]

    print(np.shape(input))


    query4 = ("INSERT INTO tensorflow_training_input "
             "VALUES (%s,%s,%s, %s, %s, %s, %s, %s, %s)")

    cursor.executemany(query4)

    cnx.commit()

populate()