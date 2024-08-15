import sys
import xml.etree.ElementTree as ET
import geopy.distance
import math
import heapq
from utils import *
import pdb
##from lxml import etree
from bs4 import BeautifulSoup

class createRequestDump:
    def __init__(self, sumoTraceFile, rateCSV, rps, maxCoverageDist):
        self.junctions = {}
        self.vehiclePositions = {}
        self.startEndDict = {}
        self.sumoTracefile = sumoTraceFile
        self.maxCoverageDist = float(maxCoverageDist)
        self.rateCSV = rateCSV
        self.rps = rps
        self.filepointer = open(rateCSV, 'w')
        

    def getClosestJunction(self, vehiclecoord):
        junctions = self.junctions
        minDist = sys.maxsize
        for junction in junctions.keys():
            junccoord = (junctions[junction][0], junctions[junction][1])
            distInMeters = geopy.distance.distance(vehiclecoord, junccoord).m
            if minDist>distInMeters:
                closestJunction = junction
                minDist=distInMeters
        if distInMeters>maxCoverageDist:
            return 'NONE'
        else:
            return closestJunction


    def allParse(self):
        sumoTracefile = self.sumoTracefile
        juncrps = {}
        timestep = -1
        self.dumpHeader()
        with open(self.sumoTracefile) as infile:
            for line in infile:
                line = line.strip()
                soup = BeautifulSoup(line)
                if(soup.timestep):
                    if timestep != -1:
                        self.dumpRPSValues(timestep-1, juncrps)
                    for junction in self.junctions.keys():
                        juncrps[junction]=0
                    timestep = int(float(soup.timestep['time']))
                    print(soup.timestep['time'])
                elif(soup.vehicle):
##                    print(soup.vehicle['id'])
                    id = soup.vehicle['id']
##                    print(id)
                    lat = float(soup.vehicle['y'])
                    lon = float(soup.vehicle['x'])

                    vehiclecoord=(lat,lon)
                    closestJunction = self.getClosestJunction(vehiclecoord)
                    if closestJunction != 'NONE':
                        juncrps[closestJunction] = juncrps[closestJunction] + self.rps

    def dumpHeader(self):
        headerJns = sorted(self.junctions.keys())
        header = ",".join(headerJns)
        header = "Timestep,"+header
        self.filepointer.write(header+"\n")


    def dumpRPSValues(self,timestep, juncrps):
        line = str(timestep)
        print(juncrps)
        for junction in sorted(self.junctions.keys()):
            if junction in juncrps.keys():
                line=line + ","+str(juncrps[junction])
        self.filepointer.write(line+"\n")
            
            

    def parseVehicles2(self):
        sumoTracefile = self.sumoTracefile
        juncrps = {}
        timestep = -1
        self.dumpHeader()
        
            
        for event, element in etree.iterparse(sumoTracefile,events=('start','end')):
            if element.tag == 'timestep' and event == 'start':
                timestep = int(float(element.attrib['time']))
##                print("======= "+element.attrib['time'])
##                pdb.set_trace()
                if(timestep!=-1):
                    self.dumpRPSValues(timestep-1, juncrps)
                for junction in self.junctions.keys():
                    juncrps[junction]=0
            
            elif element.tag == 'vehicle' and event == 'start':
                attributes = element.attrib
                id = attributes.get('id')
##                print(id)

                lat = float(attributes.get('y'))
                lon = float(attributes.get('x'))
                vehiclecoord=(lat,lon)
                closestJunction = self.getClosestJunction(vehiclecoord)
                if closestJunction != 'NONE':
                    juncrps[closestJunction] = juncrps[closestJunction] + self.rps
##            else:
##                print(event+ " MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM "+element.tag)
            element.clear()
        self.filepointer.close()


    def dumpRequestInCSV(self):
        vehiclePositions = self.vehiclePositions
        startEndDict = self.startEndDict
        for id in startEndDict.keys():
            print(startEndDict[id])
            start = int(startEndDict[id][0])*1000
            end = int(startEndDict[id][1])*1000
            for presentTimeInMillis in range(start, end-1, self.delay):
                secondVal = presentTimeInMillis / 1000
##                pdb.set_trace()
                print(start,"  ",end)
                print(secondVal)
                print(presentTimeInMillis)
##                print(vehiclePositions)
                if float(secondVal)-int(secondVal) == 0:
                    print(vehiclePositions[secondVal])
                    if id in vehiclePositions[secondVal].keys():
                        vehicleDict = vehiclePositions[secondVal][id]
                toInsertTuple = (presentTimeInMillis, id, vehicleDict[0], vehicleDict[1], vehicleDict[2], 8080)
                print(toInsertTuple)
                self.writeInCSV(toInsertTuple)


    def parseVehicles1(self):
        sumoTracefile = self.sumoTracefile
        vehiclePositions = []
        with open(sumoTracefile, 'rb') as xml_file:
            root = ET.parse(xml_file).getroot()
            for timestep in root.findall('timestep'):
                print(timestep)
                vehiclesTimeT = {}
                for vehicle in timestep.findall('vehicle'):
                    attributes = vehicle.attrib
                    id = attributes.get('id')
                    lat = float(attributes.get('y'))
                    lon = float(attributes.get('x'))
                    vehiclecoord=(lat,lon)
                    closestJunction = self.getClosestJunction(vehiclecoord)
        ##            lane = attributes.get('lane')
                    PositionTuple = (lat, lon, closestJunction)
                    vehiclesTimeT[id] = PositionTuple
        ##            print(id +"--"+posX+"--"+posY+"--"+lane)
                vehiclePositions.append( vehiclesTimeT)
            self.vehiclePositions = vehiclePositions
            return vehiclePositions

    def writeInCSV(self,rowList):
        rowStr = ",".join([str(x) for x in rowList])
        self.filepointer.write(rowStr+"\n")

    def dumpRequestInCSV1(self):
        vehiclePositions = self.vehiclePositions
        prevInd = -1
        presInd = 0
        nextInd = 1
        startendDict = {}
        csvDumpList = []
        delay = self.delay
        while presInd <len(vehiclePositions):
            if presInd ==0:
                prevDict = {}
            else:
                prevDict = vehiclePositions[prevInd]

            if presInd == len(vehiclePositions)-1:
                nextDict = {}
            else:
                nextDict = vehiclePositions[nextInd]

            presDict = vehiclePositions[presInd]

            for vehicle in [x for x in presDict if x not in prevDict]:
                startendDict[vehicle]= [presInd]

            for vehicle in [x for x in presDict if x not in nextDict]:
                startendDict[vehicle].append(nextInd)
            presInd = presInd + 1
            prevInd = prevInd + 1
            nextInd = nextInd + 1
        for id in startendDict.keys():
            presentTimeInMillis = int(startendDict[id][0]*1000) #STart Time
            endTimeInMillis = int(startendDict[id][1]*1000) #End Time
            while presentTimeInMillis<endTimeInMillis:
                presentTimeStep = int(presentTimeInMillis/1000)
                vehicleDict = vehiclePositions[presentTimeStep][id]
##                toInsertTuple = (presentTimeInMillis, id, vehicleDict[0], vehicleDict[1], vehicleDict[2], portMap[vehicleDict[2]])
                toInsertTuple = (presentTimeInMillis, id, vehicleDict[0], vehicleDict[1], vehicleDict[2], 8080)
##                csvDumpList.append(toInsertTuple)
                self.writeInCSV(toInsertTuple)
                print(toInsertTuple)
                presentTimeInMillis = presentTimeInMillis + delay
##        csvDumpList.sort(key = lambda x:x[0])
##        for row in csvDumpList:
##            self.writeInCSV(row)




            
    def createWorkflow(self):
##            self.junctions = self.ut.parseJunctions()
##            self.junctions = self.ut.parseRSUs(self.additionalFile)
        self.junctions = parseRSUs()        
        print(self.junctions)
        self.allParse()
##        self.test()
        
##        self.parseVehicles2()
        self.dumpRequestInCSV()
        self.filepointer.close()
                    


if __name__ == "__main__":
    sumoTraceFile = sys.argv[1]
    print(sumoTraceFile)
    rateCSV = sys.argv[2]
    print(rateCSV)
    rps = int(sys.argv[3])
    print(rps)
    maxCoverageDist = int(sys.argv[4])
    print(maxCoverageDist)
    crd  = createRequestDump(sumoTraceFile, rateCSV, rps, maxCoverageDist)
    crd.createWorkflow()
