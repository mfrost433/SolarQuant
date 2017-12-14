from urllib2 import Request, urlopen, URLError
import json

import datetime
import os

def getWeatherData(self):
    chunkStart = self.startDate
    while (chunkStart < self.endDate):
        chunkEnd = self.getChunkEndDate(chunkStart, self.endDate, 30)

        startString = datetime.datetime.strftime(chunkStart, "%Y-%m-%d")

        endString = datetime.datetime.strftime(chunkEnd, "%Y-%m-%d")

        request = Request(self.PREFIX + "http://api.met.no/weatherapi/locationforecast/1.9/?lat=-36.855099;lon=174.777296")
        data = ""
        try:
            response = urlopen(request)
            data = json.loads(response.read())
            with open(self.weatherFolder + '/weather_' + startString + '.json', 'w') as outfile:
                outfile.write(json.dumps(data, indent=4))
        except:
            print("Failed")
        chunkStart = chunkEnd


def getInterval(self):
    request = Request(self.PREFIX + "/solarquery/api/v1/pub/range/interval?nodeId=" + self.nodeId)
    data = ""
    try:
        response = urlopen(request)
        data = json.loads(response.read())


    except:
        print("Failed")

    return data['data']['startDate'], data['data']['endDate']