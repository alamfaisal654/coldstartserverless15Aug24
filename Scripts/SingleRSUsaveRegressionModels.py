import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
##import seaborn as sns
import os
import sys
import xml.etree.ElementTree as ET
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import ElasticNet
from sklearn import metrics
from sklearn.metrics import PredictionErrorDisplay
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from sklearn.svm import SVR
import xgboost as xg 
from utils import *
import pickle
import math

#Reading the dataset
class applyLinearReg:
    def __init__(self, numMinutes, RegrType):
        numinput = 60*numMinutes
        self.numinput = numinput
        self.RegrType = RegrType
        self.folder = "./SingleRSUDifferentKs/K"+str(numMinutes)
        self.modelFolder = self.folder+"/"+RegrType
        os.makedirs(os.path.dirname(self.modelFolder+'/abc'), exist_ok=True)
        
        self.numinput = numinput
        self.saveRegressionModels()

    def saveLinearRegression(self, RSUNum, x_train, y_train):
        print("Starting Fitting Linear Regression")
        mlr = LinearRegression()
        mlr.fit(x_train, y_train)
        print("Completed Fitting Linear Regression")
        print("Starting Saving Linear Regression")
        #mlr = pickle.load(open('modelRSU_'+str(RSUNum)+'.pkl', 'rb'))
##        y_pred= mlr.predict(data_X)

        with open(self.modelFolder+'/modelRSU_'+str(RSUNum)+'.pkl','wb') as f:
            print("Model="+'modelRSU_'+str(RSUNum))
            pickle.dump(mlr,f)
        print("Finished Saving Linear Regression")


    def savePolynomialRegression(self, RSUNum, x_train, y_train):
        print("Starting Fitting Polynomial Regression")
        poly = PolynomialFeatures(degree=2, include_bias=False)
        print("Start")
        X_poly = poly.fit_transform(x_train)
        mlr = LinearRegression()
        mlr.fit(X_poly, y_train)
        print("Completed Fitting Polynomial  Regression")
        print("Starting Saving Polynomial Regression")
        #mlr = pickle.load(open('modelRSU_'+str(RSUNum)+'.pkl', 'rb'))
##        y_pred= mlr.predict(data_X)
        with open(self.modelFolder+'/modelRSU_'+str(RSUNum)+'.pkl','wb') as f:
            print("Model="+'modelRSU_'+str(RSUNum))
            pickle.dump(mlr,f)
        print("Finished Saving Polynomial Regression")


    def saveElasticNetRegression(self, RSUNum, x_train, y_train):
        print("Starting Fitting ElasticNet Regression")
        mlr = ElasticNet(alpha=1.0, l1_ratio=0.5)
        mlr.fit(x_train, y_train)
        print("Completed Fitting ElasticNet  Regression")
        print("Starting Saving ElasticNet Regression")
        #mlr = pickle.load(open('modelRSU_'+str(RSUNum)+'.pkl', 'rb'))
##        y_pred= mlr.predict(data_X)
        with open(self.modelFolder+'/modelRSU_'+str(RSUNum)+'.pkl','wb') as f:
            print("Model="+'modelRSU_'+str(RSUNum))
            pickle.dump(mlr,f)
        print("Finished Saving ElasticNet Regression")


    def saveXGBoostRegression(self, RSUNum, x_train, y_train):
        print("Starting Fitting XGBoost Regression")
        # Instantiation 
        xgb_r = xg.XGBRegressor(n_estimators=1000, max_depth=7, eta=0.1, subsample=0.7, colsample_bytree=0.8) 
        xgb_r.fit(x_train, y_train)
        print("Completed Fitting XGBoost Regression")
        print("Starting Saving XGBoost Regression")
        #mlr = pickle.load(open('modelRSU_'+str(RSUNum)+'.pkl', 'rb'))
##        y_pred= mlr.predict(data_X)
        with open(self.modelFolder+'/modelRSU_'+str(RSUNum)+'.pkl','wb') as f:
            print("Model="+'modelRSU_'+str(RSUNum))
            pickle.dump(xgb_r,f)
        print("Finished Saving XGBoost Regression")


    def saveRandomForestRegression(self, RSUNum, x_train, y_train):
        print("Starting Fitting RandomForest Regression")
        mlr = RandomForestRegressor(n_estimators=10, random_state=0, oob_score=True)
        mlr.fit(x_train, y_train)
        print("Completed Fitting RandomForest Regression")
        print("Starting Saving RandomForest Regression")
        #mlr = pickle.load(open('modelRSU_'+str(RSUNum)+'.pkl', 'rb'))
##        y_pred= mlr.predict(data_X)
        with open(self.modelFolder+'/modelRSU_'+str(RSUNum)+'.pkl','wb') as f:
            print("Model="+'modelRSU_'+str(RSUNum))
            pickle.dump(mlr,f)
        print("Finished Saving RandomForest Regression")


    def saveRandomForestRegression(self, RSUNum, x_train, y_train):
        print("Starting Fitting RandomForest Regression")
        mlr = RandomForestRegressor(n_estimators=10, random_state=0, oob_score=True)
        mlr.fit(x_train, y_train)
        print("Completed Fitting RandomForest Regression")
        print("Starting Saving RandomForest Regression")
        #mlr = pickle.load(open('modelRSU_'+str(RSUNum)+'.pkl', 'rb'))
##        y_pred= mlr.predict(data_X)
        with open(self.modelFolder+'/modelRSU_'+str(RSUNum)+'.pkl','wb') as f:
            print("Model="+'modelRSU_'+str(RSUNum))
            pickle.dump(mlr,f)
        print("Finished Saving RandomForest Regression")

    def saveDecisionTreeRegression(self, RSUNum, x_train, y_train):
        print("Starting Fitting DecisionTree Regression")
        mlr = DecisionTreeRegressor(random_state = 0)  
        mlr.fit(x_train, y_train)
        print("Completed Fitting DecisionTree Regression")
        print("Starting Saving DecisionTree Regression")
        #mlr = pickle.load(open('modelRSU_'+str(RSUNum)+'.pkl', 'rb'))
##        y_pred= mlr.predict(data_X)
        with open(self.modelFolder+'/modelRSU_'+str(RSUNum)+'.pkl','wb') as f:
            print("Model="+'modelRSU_'+str(RSUNum))
            pickle.dump(mlr,f)
        print("Finished Saving DecisionTree Regression")


    def saveSVRRegression(self, RSUNum, x_train, y_train):
        print("Starting Fitting SVR Regression")
        mlr =SVR(kernel='rbf') 
        mlr.fit(x_train, y_train)
        print("Completed Fitting SVR Regression")
        print("Starting Saving SVR Regression")
        #mlr = pickle.load(open('modelRSU_'+str(RSUNum)+'.pkl', 'rb'))
##        y_pred= mlr.predict(data_X)
        with open(self.modelFolder+'/modelRSU_'+str(RSUNum)+'.pkl','wb') as f:
            print("Model="+'modelRSU_'+str(RSUNum))
            pickle.dump(mlr,f)
        print("Finished Saving SVR Regression")


    def saveMLPRegression(self, RSUNum, x_train, y_train):
        print("Starting Fitting MLP Regression")
        sc=StandardScaler()
        scaler = sc.fit(x_train)
        trainX_scaled = scaler.transform(x_train)
        mlr = MLPRegressor(hidden_layer_sizes=(150,100,50),
                       max_iter = 300,activation = 'relu',
                       solver = 'adam')
        mlr.fit(trainX_scaled, y_train)
        print("Completed Fitting MLP Regression")
        print("Starting Saving MLP Regression")
        #mlr = pickle.load(open('modelRSU_'+str(RSUNum)+'.pkl', 'rb'))
##        y_pred= mlr.predict(data_X)
        with open(self.modelFolder+'/modelRSU_'+str(RSUNum)+'.pkl','wb') as f:
            print("Model="+'modelRSU_'+str(RSUNum))
            pickle.dump(mlr,f)
        print("Finished Saving MLP Regression")



    def saveRegressionModels(self):
        print("Reading Dataset")
        numJunctions = self.getNumJunctions()
        numX = self.numinput
        print(self.numinput)
        print(numX)
        X_header = ['X_'+str(x) for x in range(numX)]
        for RSUNum in range(numJunctions):
            self.dataset = self.folder+'/TrainingDatasetRSU'+str(RSUNum)+'.csv'
            df = pd.read_csv(self.dataset, sep=',', engine='c', na_filter=False, dtype=np.int16, low_memory=False)
            print("Completed Reading Dataset"+"==="+str(type(df.iloc[1,1])))
            data_X = df[X_header]
            data_y = df['Y_0']
            # x_train, x_test, y_train, y_test = train_test_split(data_X, data_y, test_size = 0.3, random_state = 100)
            x_train, y_train = (data_X, data_y)
            if self.RegrType == "Linear":
                self.saveLinearRegression(RSUNum, x_train, y_train)
            elif self.RegrType == "Poly":
                self.savePolynomialRegression(RSUNum, x_train, y_train)
            elif self.RegrType == "Elastic":
                self.saveElasticNetRegression(RSUNum, x_train, y_train)
            elif self.RegrType == "XGBoost":
                self.saveXGBoostRegression(RSUNum, x_train, y_train)
            elif self.RegrType == "RandomForest":
                self.saveRandomForestRegression(RSUNum, x_train, y_train)
            elif self.RegrType == "DTR":
                self.saveDecisionTreeRegression(RSUNum, x_train, y_train)
            elif self.RegrType == "SVR":
                self.saveSVRRegression(RSUNum, x_train, y_train)
            elif self.RegrType == "MLP":
                self.saveMLPRegression(RSUNum, x_train, y_train)
            else:
                print("Incorrect Model Mentioned")
                exit()

    def getNumJunctions(self):
        junctions = parseRSUs()
        return len(junctions.keys())
        
if __name__ == "__main__":
    numMinutes = int(sys.argv[1])
    RegrType = sys.argv[2]
    alr = applyLinearReg( numMinutes, RegrType)
    
    
    
