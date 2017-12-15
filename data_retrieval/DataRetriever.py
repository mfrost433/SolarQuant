from urllib2 import Request, urlopen, URLError
import json

import datetime
import os
directory = os.path.dirname(__file__)
print(directory)
class DataRetriever():

#
#WEATHER DATUM DOES NOT GO BACK FAR ENOUGH - 2015 IS EARLIEST
#
#
#
#


    PREFIX = "https://data.solarnetwork.net"
    def __init__(self, nodeId, srcId, startDate, endDate):

        self.nodeId = nodeId
        self.srcId = srcId
        self.chunksFolder = os.path.join(directory, "chunks/")
        self.weatherFolder = os.path.join(directory, "weather/")
        startDateI, endDateI = self.getInterval()

        #if the difference between the last datum and the current date is too large, fail.
        if(abs((datetime.datetime.strptime(endDateI, "%Y-%m-%d %M:%S") - datetime.datetime.utcnow()).days) > 15):
            print(datetime.datetime.strptime(endDateI, "%Y-%m-%d %M:%S") - datetime.datetime.utcnow().days)
            print(startDateI)
            print(datetime.datetime.utcnow())


            raise Exception


        if((startDate == None) | (endDate == None)):

            if(datetime.datetime.strptime(startDateI, "%Y-%m-%d %M:%S") < datetime.datetime.strptime("2015-01-01 00:00","%Y-%m-%d %M:%S")):
                self.startDate = datetime.datetime.strptime("2015-01-01 00:00","%Y-%m-%d %M:%S")
            else:
                self.startDate = datetime.datetime.strptime(startDateI, "%Y-%m-%d %M:%S")
            self.endDate = datetime.datetime.strptime(endDateI, "%Y-%m-%d %M:%S")

        else:
            self.startDate = datetime.datetime.strptime(startDate,"%Y-%m-%d:%H:%M")
            self.endDate = datetime.datetime.strptime(endDate,"%Y-%m-%d:%H:%M")

    def getChunkEndDate(self, current, endDate, minInterval):
        out = current + datetime.timedelta(minutes=500*minInterval)
        if(out > endDate):
            return endDate
        else:
            return out

    def getNodeData(self):

        chunkStart = self.startDate
        while (chunkStart < self.endDate):
            chunkEnd = self.getChunkEndDate(chunkStart,self.endDate, 20)

            startString = datetime.datetime.strftime(chunkStart,"%Y-%m-%dT12%%3A00")

            endString = datetime.datetime.strftime(chunkEnd, "%Y-%m-%dT12%%3A00")

            request = Request(self.PREFIX + "/solarquery/api/v1/pub/datum/"
                              "list?nodeId="+self.nodeId+"&aggregation=ThirtyMinute&startDate="+
                              startString+"&endDate="+endString+"&sourceIds="+self.srcId+"&max=5000000")
            data = ""
            try:

                response = urlopen(request)
                data = json.loads(response.read())
                with open(self.chunksFolder+'chunk_'+ startString+'.json', 'w') as outfile:

                    outfile.write(json.dumps(data, indent=4))
            except:
                print("Failed")
            chunkStart = chunkEnd



    def getWeatherData(self):

        chunkStart = self.startDate
        while (chunkStart < self.endDate):
            chunkEnd = self.getChunkEndDate(chunkStart, self.endDate, 30)

            startString = datetime.datetime.strftime(chunkStart,"%Y-%m-%d")

            endString = datetime.datetime.strftime(chunkEnd, "%Y-%m-%d")


            request = Request(self.PREFIX+"/solarquery/api/v1/pub/location/datum/list?locationId=301025&sourceIds="
                              "NZ%20MetService&offset=0&"
                              "startDate=" + startString + "&endDate=" + endString)
            data = ""
            try:
                response = urlopen(request)
                data = json.loads(response.read())
                with open(self.weatherFolder+'/weather_'+ startString+'.json', 'w') as outfile:
                    outfile.write(json.dumps(data, indent=4))
            except:
                print("Failed")
            chunkStart = chunkEnd


    def getInterval(self):
        request = Request(self.PREFIX + "/solarquery/api/v1/pub/range/interval?nodeId="+self.nodeId)
        data = ""
        try:
            response = urlopen(request)
            data = json.loads(response.read())


        except:
            print("Failed")

        return data['data']['startDate'], data['data']['endDate']