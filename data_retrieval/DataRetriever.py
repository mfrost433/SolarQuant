from urllib2 import Request, urlopen, URLError
import json

import datetime
import os

directory = os.path.dirname(__file__)
print(directory)
class DataRetriever():



    PREFIX = "https://data.solarnetwork.net"
    def __init__(self, nodeId, srcId, startDate, endDate):

        self.nodeId = nodeId
        self.srcId = srcId
        self.chunksFolder = os.path.join(directory, "chunks/")
        self.weatherFolder = os.path.join(directory, "weather/")
        if((startDate == None) | (endDate == None)):
            startDate, endDate = self.getInterval()
            self.startDate = datetime.datetime.strptime(startDate,"%Y-%m-%d %M:%S")
            self.endDate = datetime.datetime.strptime(endDate, "%Y-%m-%d %M:%S")
            print(startDate)
            print(endDate)

        else:
            self.startDate = datetime.datetime.strptime(startDate,"%Y-%m-%d")
            self.endDate = datetime.datetime.strptime(endDate,"%Y-%m-%d")

    def getChunkEndDate(self, current, endDate, minInterval):
        out = current + datetime.timedelta(minutes=500*minInterval)
        if(out > endDate):
            return endDate
        else:
            return out

    def getNodeData(self):

        chunkStart = self.startDate
        while (chunkStart < self.endDate):

            chunkEnd = self.getChunkEndDate(chunkStart,self.endDate, 10)

            startString = datetime.datetime.strftime(chunkStart,"%Y-%m-%dT12%%3A00")

            endString = datetime.datetime.strftime(chunkEnd, "%Y-%m-%dT12%%3A00")

            request = Request(self.PREFIX + "/solarquery/api/v1/pub/datum/"
                              "list?nodeId="+self.nodeId+"&aggregation=Hour&startDate="+
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
           # print()
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