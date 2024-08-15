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
#        self.folder = "./DifferentKs/K"+str(numinput)
#        self.modelFolder = self.folder+"/"+RegrType
#        print(self.modelFolder)
#        self.dataset = self.folder+'/TrainingDataset.csv'
#        self.numinput = numinput
#        self.RegrType = RegrType
##        if self.RegrType == "Linear":
##            self.folder = "LinearRegression"
##        elif self.RegrType == "Poly":
##            self.folder = "PolyRegression"
##        elif self.RegrType == "Elastic":
##            self.folder = "ElasticNetRegression"
##        elif self.RegrType == "XGBoost":
##            self.folder = "XGBoostRegression"
##        elif self.RegrType == "RandomForest":
##            self.folder = "RandomForestRegression"
##        elif self.RegrType == "SVR":
##            self.folder = "SVRRegression"
##        elif self.RegrType == "MLP":
##            self.folder = "MLPRegression"
##        else:
##            print("Incorrect Model Mentioned")
        self.applyLinearRegressionModels()
##        self.generateRegressionMSEReport()

    def applyLinearRegressionModels(self):
        print("Reading Data")
        df = pd.read_csv("DifferentKs/K12/TestingMSEDataset.csv")
        print("Read The Data")
        numminutes = 12
        RegrType = "Elastic"
        numJunctions = self.getNumJunctions()
        numX = numminutes* 60 * numJunctions
        X_header = ['X_'+str(x) for x in range(numX)]
        print(X_header)
        data_X = df[X_header]
        for RSUNum in range(numJunctions):
            data_y = df['Y_'+str(RSUNum)]
            x_train, y_train = (data_X, data_y)
            mlr = pickle.load(open('DifferentKs/K'+str(numminutes)+'/'+RegrType+'/modelRSU_'+str(RSUNum)+'.pkl', 'rb'))
            y_pred= mlr.predict(data_X)
            f = open("DifferentKs/K"+str(numminutes)+"/"+RegrType+"/RSUPrediction_"+str(RSUNum)+".json", "w")
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
    alr = applyLinearReg()
    
    
    
