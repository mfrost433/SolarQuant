import os
from urllib2 import Request, urlopen, URLError
import datetime as dt
import csv
import mysql.connector
import json
requestIds = []

cnx = mysql.connector.connect(user='solarquant', password='solarquant',
                              host='localhost',
                              database='solarquant')
cursor = cnx.cursor()

directory = os.path.dirname(__file__)
for the_file in os.listdir(directory):
    try:
        if(the_file.find("prediction")):
            word = the_file.split("_")
            requestIds.append(int(word[0]))
    except:
        1


def getPredictionRequestInfo(requestId):
    query = ("SELECT * FROM prediction_requests "
             "WHERE REQUEST_ID = {}")

    query = query.format(requestId)

    cursor.execute(query)

    data = cursor.fetchall()[0]


    nodeId = data[1]
    sourceId = data[2]
    dateRequested = data[3]
    return nodeId, sourceId, dateRequested

for i in requestIds:
    try:
        nodeId, srcId, dateRequested = getPredictionRequestInfo(i)
        endDate = dateRequested + dt.timedelta(days=7)
        dateRequested = dateRequested - dt.timedelta(days=1)
        startString = dateRequested.strftime("%Y-%m-%dT12%%3A00")
        endDate = dateRequested + dt.timedelta(days=7)
        endString = endDate.strftime("%Y-%m-%dT12%%3A00")

        request = "https://data.solarnetwork.net/solarquery/api/v1/pub/datum/list?nodeId=" + str(nodeId) + "&aggregation=ThirtyMinute&startDate=" + \
                  startString + "&endDate=" + endString + "&sourceIds=" + srcId + "&max=5000000"
        response = urlopen(request)
        with open(str(i) + '_real.csv', 'w') as outfile:
            outfile.write("created,wattHours\n")
            try:

                data = json.loads(response.read())
                for line in data["data"]["results"]:
                    date = dt.datetime.strptime(line["created"], "%Y-%m-%d %H:%M:%S.%fZ")
                    date = date.strftime("%Y-%m-%dT%H:%M:%S.00Z")
                    string = str(date) + "," + str(line["wattHours"]) + "\n"
                    outfile.write(string)

            except Exception as e:
                print(e)
    except Exception as e:
        print(e)

