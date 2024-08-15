import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
##import seaborn as sns
import sys
import xml.etree.ElementTree as ET
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn import metrics
from sklearn.metrics import PredictionErrorDisplay
from sklearn.linear_model import LinearRegression


#Reading the dataset
class applyPolunomialReg:
    def __init__(self,sumoNetfile, dataset, numinput):
        self.sumoNetfile = sumoNetfile
        self.dataset = dataset
        self.numinput = numinput
        self.performPolynomialRegression()


    def performPolynomialRegression(self):
        df = pd.read_csv(self.dataset)
        numJunctions = self.getNumJunctions()
        numX = self.numinput * numJunctions
        print(numX)
        X_header = ['X_'+str(x) for x in range(numX)]
        print(X_header)
        data_X = df[X_header]
        data_y = df['Y_1']
        print(data_X.shape)
        poly = PolynomialFeatures(degree=3, include_bias=False)
        poly_features = poly.fit_transform(data_X)
        x_train, x_test, y_train, y_test = train_test_split(data_X, data_y, test_size = 0.3, random_state = 100)
        
        poly_reg_model = LinearRegression()
        poly_reg_model.fit(x_train, y_train)
        
##        mlr.fit(_train, y_train)
        y_pred= poly_reg_model.predict(x_test)
        mlr_diff = pd.DataFrame({'Actual value': y_test, 'Predicted value': y_pred})
        print(mlr_diff.to_string())
        print(metrics.mean_absolute_error(y_test,y_pred))
        print(np.sqrt(metrics.mean_squared_error(y_test,y_pred)))
        display = PredictionErrorDisplay.from_predictions(y_true=y_test, y_pred=y_pred)
##        display.plot()
        plt.show()



    def getNumJunctions(self):
        junctions = {}
        sumoNetfile = self.sumoNetfile
        root = ET.parse(sumoNetfile).getroot()
        for junction in root.findall('junction'):
            attributes = junction.attrib
            id = attributes.get('id')
            posX = float(attributes.get('x'))
            posY = float(attributes.get('y'))
            type = attributes.get('type')
    ##        print(str(id)+"==="+str(type))
            if type not in ['dead_end','internal']:
                junctions[id]=(posX,posY)
    ##    print(len(junctions))
    ##    print(junctions)
##        self.junctions = junctions
        return len(junctions.keys())
        

if __name__ == "__main__":
    sumoNetfile = sys.argv[1]
    print(sumoNetfile)
    dataset = sys.argv[2]
    print(dataset)
    numinput = int(sys.argv[3])
    print(numinput)
    alr = applyPolunomialReg(sumoNetfile, dataset, numinput)
    
    
    
