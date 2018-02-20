from optparse import OptionParser
import argparse
import mysql.connector
from subprocess import call
import logging
import os
from training import GenerateTrainingFile as gen
from prediction import GeneratePredictionData as genP
import PlotData as plt
import traceback as tb
import training.DatabaseCorrelation as dc
import prediction.DatabasePrediction as dp
import datetime
dir = os.path.dirname(__file__)

cnx = mysql.connector.connect(user='solarquant', password='solarquant',
                              host='localhost',
                              database='solarquant')
cursor = cnx.cursor()

parser = OptionParser()
argParser = argparse.ArgumentParser()
argParser.add_argument("-r", "--reqid", dest="reqId", help="ID for request",
                  metavar = "ID", required = True)

argParser.add_argument("-t", "--train", action = 'store_true', dest="mode", help="MODE for request - train(t) or predict", default=True)

argParser.add_argument("-p", "--predict", action = 'store_false', dest="mode", help="MODE for request - train or predict")

args = argParser.parse_args()
file = os.path.join(dir, 'example.log'.format(args.reqId))
logging.basicConfig(filename=file, filemode='w', level=logging.DEBUG)


def getRequestParameters(type):
    query = ("SELECT NODE_ID, SOURCE_ID FROM {}_requests WHERE REQUEST_ID = %s".format(type))
    cursor.execute(query, (args.reqId,))
    out = cursor.fetchall()[0]
    return out[0], out[1]

def log_end_time(type):
    ctime = datetime.datetime.now()
    query = ("UPDATE {}_state_time SET COMPLETION_DATE=%s WHERE REQUEST_ID=%s AND STATE=%s".format(type))
    cursor.execute(query, (ctime, args.reqId, 3))
    cnx.commit()

try:
    if(args.mode):
        nodeId, srcId = getRequestParameters("training")
        file = os.path.join(dir, "../run.sh")

        gen.generate(args.reqId)
        print('done')
        call([file,args.reqId, str(nodeId), srcId])

        file = os.path.join(dir, "../test.sh")
        call([file, args.reqId, str(nodeId), srcId])

        plt.setupTrainingOutput(args.reqId)
        dc.store_correlation(request_id=args.reqId)
        log_end_time("training")

    else:
        nodeId, srcId = getRequestParameters("prediction")
        file = os.path.join(dir, "../predict.sh")
        genP.generate(args.reqId)
        call([file, args.reqId, str(nodeId), str(srcId)])
        plt.setupPredictionOutput(args.reqId)
        dp.store_correlation(request_id=args.reqId)
        print("storin")
        log_end_time("prediction")

except Exception as e:
    logging.info(str(e))
    tb.print_exc(e)

