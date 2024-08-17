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
class applyLinearReg:
    def __init__(self):
##        self.applyLinearRegressionModels()
        self.generateRegressionMSEReport()

    def applyLinearRegressionModels(self):
        numminutes = 12
        RegrType = "Elastic"
        numJunctions = self.getNumJunctions()
        for RSUNum in range(numJunctions):
            folder = "./SingleRSUDifferentKs/K"+str(numminutes)
            modelFolder = folder+"/"+RegrType
            print("Reading Data")
            df = pd.read_csv(folder+"/TestingRegressionDatasetRSU"+str(RSUNum)+".csv")
            print("Read The Data")
            numX = numminutes* 60
            X_header = ['X_'+str(x) for x in range(numX)]
            print(X_header)
            data_X = df[X_header]
            data_y = df['Y_0']
            x_train, y_train = (data_X, data_y)
            mlr = pickle.load(open(modelFolder+'/modelRSU_'+str(RSUNum)+'.pkl', 'rb'))
            y_pred= mlr.predict(data_X)
            f = open(modelFolder+"/RSUPrediction_"+str(RSUNum)+".json", "w")
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
        fileLog = open('SingleRSUgenerateRegressionMSEReport.csv', 'w')
        numJunctions = self.getNumJunctions()
        numMinutesList=[x for x in range(2,21,2)]
        RegrTypeList = ["Linear","Elastic","XGBoost",
                        "RandomForest","DTR"]
        for RegrType in RegrTypeList:
            for numminutes in numMinutesList:
                numinput = 60 * numminutes
                print(RegrType)
                print(numinput)
                folder = "./SingleRSUDifferentKs/K"+str(numminutes)
                modelFolder = folder+"/"+RegrType
                for RSUNum in range(numJunctions):
                    dataset = folder+'/TestingMSEDatasetRSU'+str(RSUNum)+'.csv'
                    df = pd.read_csv(dataset)
                    numX = numinput
                    X_header = ['X_'+str(x) for x in range(numX)]
                    data_X = df[X_header]
                    data_y = df['Y_0']
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
    alr = applyLinearReg()
    
    
    
