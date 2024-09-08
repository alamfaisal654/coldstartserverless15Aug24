import sys
import  pandas as pd
from utils import *

class createDataSet:
    def __init__(self,ratecsv, datasetfolder, num_input_minutes,
                 num_output_minutes, precursor):
        self.ratecsv = ratecsv
        self.num_input_minutes = num_input_minutes
        self.num_input_rows = 60*num_input_minutes
        self.num_output_rows = 60*num_output_minutes
        self.precursor = precursor
        self.datasetfolder = datasetfolder
        # self.datasetfolder = datasetfolder+"/K"+str(num_input_minutes)
        self.numJunctions = self.getNumJunctions()
        for junction in range(self.numJunctions):
            filename = self.datasetfolder+"/"+precursor+"RSU"+str(junction)+".csv"
            self.file_pointer = open(filename,'w')
            self.parseCSV(junction)
            self.file_pointer.close()

    def addHeader(self, row):
##        numJunctions=len(row.split(','))
        numJunctions = self.numJunctions
        header_list_X = ['X_'+str(x) for x in range(self.num_input_rows)]
        header_list_Y = ['Y_0']
        header_list = header_list_X + header_list_Y
        header=','.join(header_list)
        header='Timestep'+','+header
        self.file_pointer.write(header+'\n')

    def dumpRow(self,timestep, input_rows,processed_output):
        processed_output = [str(x) for x in processed_output]
        input_rows.append(','.join(processed_output))
##        print(input_rows)
        row = ','.join(input_rows)
        row=timestep+","+row
        self.file_pointer.write(row+'\n')
        
        

    def parseCSV(self, junction):
        print( "Junction="+str(junction))
        fp = open(ratecsv,'r')
        data = fp.readlines()[1:]
        #Remove first column of seconds as sno
        timestep = [x.split(',')[0] for x in data]
        data = [x.split(',')[junction+1] for x in data]
        self.addHeader(data[0])
        numrows=len(data)
        removerows = 0
        num_input_rows = self.num_input_rows
        num_output_rows = self.num_output_rows
        
        for row in range(num_input_rows, numrows-num_output_rows):
##            print("row no="+str(timestep))
            input_rows = [data[x].strip() for x in range(row-num_input_rows, row)]
##            print(input_rows)
            output_rows=[data[x].strip() for x in range(row,row+num_output_rows)]
##            print(output_rows)
            processed_output = self.getMeanFromRows(output_rows)
            self.dumpRow(timestep[row], input_rows,processed_output)
        
    def getMeanFromRows(self,output_rows):
        df = pd.DataFrame([x.split(",") for x in output_rows])
##        print(df)
        df = df.astype('int').bfill()
        
##        df2 = df.mean(axis=0)
        df2 = df.max(axis=0)
        meanlist=df2.values.tolist()
        # print(meanlist)
        return meanlist

    def getNumJunctions(self):
        junctions = parseRSUs()
        return len(junctions.keys())

    

            

if __name__ == "__main__":
    ratecsv = sys.argv[1]
    print(ratecsv)
    datasetfolder = sys.argv[2]
    print(datasetfolder)
    num_input_minutes = int(sys.argv[3])
    num_output_minutes = int(sys.argv[4])
    precursor = sys.argv[5]
    
    grps  = createDataSet(ratecsv, datasetfolder, num_input_minutes,
                          num_output_minutes, precursor)
