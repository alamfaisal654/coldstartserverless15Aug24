import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
##import seaborn as sns
import sys
import xml.etree.ElementTree as ET
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from sklearn.metrics import PredictionErrorDisplay
from utils import *
import pickle
import math
from sklearn.metrics import mean_squared_error
from pathlib import Path

#Reading the dataset
class applyRegressionModels:
    def __init__(self, datasetname, num_input_minutes, num_output_minutes, RegrType):
        self.num_input_minutes = num_input_minutes
        self.num_input_rows = 60*num_input_minutes
        self.num_output_rows = 60*num_output_minutes
        self.datasetfolder = "./AllDatasets/Last"+str(num_input_minutes)+"/Future"+str(num_output_minutes)
        self.modelFolder = self.datasetfolder+"/"+RegrType
        self.dataset = self.datasetfolder+"/"+datasetname
        print(self.modelFolder)

        self.applyRegression()
##        self.generateRegressionMSEReport()

    def applyRegression(self):
        print("Reading Data")
        df = pd.read_csv(self.dataset)
        numJunctions = self.getNumJunctions()
        numX = self.num_input_rows * numJunctions
        X_header = ['X_'+str(x) for x in range(numX)]
        print(X_header)
        data_X = df[X_header]
        for RSUNum in range(numJunctions):
            data_y = df['Y_'+str(RSUNum)]
            x_train, y_train = (data_X, data_y)
            model = self.modelFolder+'/modelRSU_'+str(RSUNum)+'.pkl'
            mlr = pickle.load(open(model, 'rb'))
            y_pred= mlr.predict(data_X)
            f = open(self.modelFolder+"/RSUPrediction_"+str(RSUNum)+".json", "w")
            f.write("{"+'\n')
            count = 0
            numRows,numcols = data_X.shape
            for ind in data_X.index:
                str12 = "\""+str(df['Timestep'][ind])+"\"" + ":" + "\""+str(math.ceil(y_pred[ind]))+"\","
                if count==numRows-1:
                    str12 = "\""+str(df['Timestep'][ind])+"\"" + ":" + "\""+str(math.ceil(y_pred[ind]))+"\""
                f.write(str12+'\n')
                print(str12)
                count = count + 1
            f.write("}"+'\n')
            f.close()

    def generateRegressionMSEReport(self):
        fileLog = open('generateRegressionMSEReport.csv', 'w')
        numJunctions = self.getNumJunctions()
        numMinutesList=[x for x in range(2,21,2)]
        RegrTypeList = ["Linear","Elastic","XGBoost",
                        "RandomForest","DTR","MLP"]
        for RegrType in RegrTypeList:
            for numminutes in numMinutesList:
                numinput = 60 * numminutes
                print(RegrType)
                print(numinput)
                folder = "./DifferentKs/K"+str(numminutes)
                modelFolder = folder+"/"+RegrType
                dataset = folder+'/TestingMSEDataset.csv'
                df = pd.read_csv(dataset)
                numX = numinput * numJunctions
                X_header = ['X_'+str(x) for x in range(numX)]
                data_X = df[X_header]
                for RSUNum in range(numJunctions):
                    data_y = df['Y_'+str(RSUNum)]
                    x_train, y_train = (data_X, data_y)
                    modelfile = modelFolder+'/modelRSU_'+str(RSUNum)+'.pkl'
                    my_file = Path(modelfile)
                    if my_file.is_file():
                        mlr = pickle.load(open(modelfile, 'rb'))
    ##                    print(mlr.feature_names)
                        y_pred= mlr.predict(data_X)
                        mse = mean_squared_error(y_train,y_pred)
                        line = RegrType+","+str(numinput)+",RSU_"+str(RSUNum)+","+str(mse)
                        print(line)
                        fileLog.write(line+'\n')
                    else:
                        print(str(modelfile)+ "  not present")
                        fileLog.write(str(modelfile)+ "  not present"+'\n')
        fileLog.close()


    def getNumJunctions(self):
        junctions = parseRSUs()
        return len(junctions.keys())
        

if __name__ == "__main__":
    datasetname = sys.argv[1]
    print(datasetname)
    num_input_minutes = int(sys.argv[2])
    num_output_minutes = int(sys.argv[3])
    RegrType = sys.argv[4]
    alr = applyRegressionModels(datasetname, num_input_minutes, num_output_minutes, RegrType)
    
    
    
