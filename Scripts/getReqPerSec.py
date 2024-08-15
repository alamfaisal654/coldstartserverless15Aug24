import sys
import pandas as pd
import xml.etree.ElementTree as ET
from utils import * 

class getReqPerSec:
    def __init__(self, reqcsv, ratedumpcsv):
        self.reqcsv = reqcsv
        self.ratedumpcsv = ratedumpcsv
##        ut =  utils(sumoNetfile)
        self.junctions = parseRSUs()
##        self.junctions = ut.parseRSUs(self.additionalFile)
        self.fileptr = open(ratedumpcsv,'w')
        headers = 'seconds,'+','.join(self.junctions)
        self.fileptr.write(headers+'\n')
        self.getAllReqs()
        self.fileptr.close()



    def dumpInCsv(self,second,junctions_dict):
##        print(junctions_dict)
        numReqs=[str(second)]
##        print('------------------------------------------------------------------')
##        print(self.junctions.keys())
##        print(junctions_dict.keys())
        for jn in self.junctions:
##            print(jn)
##            print(type(jn))
##            print(junctions_dict[jn])
##            print(junctions_dict)
            numReqs.append(str(junctions_dict[jn]))
        line = ','.join(numReqs)
##        print(line)
        self.fileptr.write(line+'\n')
        
            
    
    def getAllReqs(self):
        df = pd.read_csv(self.reqcsv,
                         names=["msec", "id", "lat", "lon",'jn','port'])
        df["jn"]=df["jn"].apply(str)
        maxmsec = df['msec'].max().item()
        startmsec=0
        endmsec=1000
        seconds=1
        while(startmsec < maxmsec):
            sliceddf=df[df['msec'].between(startmsec, endmsec, inclusive="left")]
##            print(sliceddf)
            countdf=sliceddf.groupby(['jn']).size().reset_index(name='counts')
##            print(countdf)
            junctions_dict = dict(zip(self.junctions, [0]*len(self.junctions)))
##            print(junctions_dict)
            for index, row in countdf.iterrows():
##                print(row)
                jn=str(row['jn'])
##                print(jn)
                count=row['counts']
                if jn != 'None':
                    junctions_dict[jn] = count
##                print(jn)
##                print(count)
##            print(junctions_dict)
            self.dumpInCsv(seconds,junctions_dict)
            startmsec = startmsec + 1000
            endmsec = endmsec + 1000
            seconds = seconds + 1

        


if __name__ == "__main__":
    reqcsv = sys.argv[1]
    print(reqcsv)
    ratedumpcsv = sys.argv[2]
    print(ratedumpcsv)
    grps  = getReqPerSec(reqcsv, ratedumpcsv)
