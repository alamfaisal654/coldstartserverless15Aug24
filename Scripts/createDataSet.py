import sys
import  pandas as pd
import os

class createDataSet:
    def __init__(self,ratecsv, dataset, num_input_minutes, num_output_minutes):
        self.ratecsv = ratecsv
        self.num_input_rows = 60*num_input_minutes
        self.num_output_rows = 60*num_output_minutes
        self.dataset = dataset
        os.makedirs(os.path.dirname(dataset), exist_ok=True)
        self.file_pointer = open(dataset,'w')
        self.parseCSV()
        self.file_pointer.close()

    def addHeader(self, row):
        numJunctions=len(row.split(','))
        header_list_X = ['X_'+str(x) for x in range(numJunctions*self.num_input_rows)]
        header_list_Y = ['Y_'+str(x) for x in range(numJunctions)]
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
        
        

    def parseCSV(self):
        fp = open(ratecsv,'r')
        data = fp.readlines()[1:]
        #Remove first column of seconds as sno
        timestep = [x.split(',')[0] for x in data]
        data = [','.join(x.split(',')[1:]) for x in data]
        self.addHeader(data[0])
        numrows=len(data)
        removerows = 0
        num_input_rows = self.num_input_rows
        num_output_rows = self.num_output_rows
##        print(numrows)
        for row in range(num_input_rows, numrows-num_output_rows):
            input_rows = [data[x].strip() for x in range(row-num_input_rows, row)]
##            print(input_rows)
            output_rows=[data[x].strip() for x in range(row,row+num_output_rows)]
##            print(output_rows)
            processed_output = self.getMeanFromRows(output_rows)
            self.dumpRow(timestep[row], input_rows,processed_output)
        
    def getMeanFromRows(self,output_rows):
        df = pd.DataFrame([x.split(",") for x in output_rows])
        df = df.astype('int')
##        df2 = df.mean(axis=0)
        df2 = df.max(axis=0)
        meanlist=df2.values.tolist()
        # print(meanlist)
        return meanlist
    

            

if __name__ == "__main__":
    ratecsv = sys.argv[1]
    print(ratecsv)
    dataset = sys.argv[2]
    print(dataset)
    num_input_minutes = int(sys.argv[3])
    num_output_minutes = int(sys.argv[4])
    
    
    grps  = createDataSet(ratecsv, dataset, num_input_minutes, num_output_minutes)
