import sys
import xml.etree.ElementTree as ET
import math
import heapq
from geopy.distance import geodesic
import sumolib

class utils:
    def __init__(self, sumoNetfile):
        self.sumoNetfile = sumoNetfile
        (self.sumoBBox, self.osmBBox, self.metersDim) = self.getDimensionsMetsAndOsm()
        self.net = sumolib.net.readNet(sumoNetfile)
        
        

    def parseJunctions(self):
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
            if type in ['traffic_light']:
                junctions[id]=(posX,posY)
    ##    print(len(junctions))
    ##    print(junctions)
    ##    self.junctions = junctions
        print(junctions)
        return junctions

    def parseRSUs(self, xmlFile):
        junctions = {}
        sumoNetfile = self.sumoNetfile
        root = ET.parse(xmlFile).getroot()
        for poi in root.findall('poi'):
            attributes = poi.attrib
            id = attributes.get('id')
            posX = float(attributes.get('x'))
            posY = float(attributes.get('y'))
            junctions[id]=(posX,posY)
        return junctions
            


    #Get the Map dimensions from sumo to osm
    def getDimensionsMetsAndOsm(self):
        print("Getting map dimensions")
        sumoNetfile = self. sumoNetfile
        (sumoBBox, osmBBox) = self.getMapDimensions( )
        (longLeft, latTop, longRight, latBottom) = osmBBox
##        coords_1 = ( latTop, longLeft)
##        coords_2 = ( latTop, longRight)
##        print("hello=%s %s" %( coords_1, coords_2))
##        metersHorizontal = geodesic(coords_1, coords_2).meters
##    ##    metersHorizontal = 1000
##        coords_1 = ( latTop, longLeft)
##        coords_2 = ( latBottom, longLeft)
##        metersVertical = geodesic(coords_1, coords_2).meters
##    ##    metersVertical = 1000


        ######HARDCODED VALUES#######
        metersHorizontal = 8457
        metersVertical = 8258
        print(sumoBBox)
        print(type(longLeft))
        print(osmBBox)
        print((metersHorizontal, metersVertical))
        print(type(metersHorizontal))
        return(sumoBBox, osmBBox, (metersHorizontal, metersVertical))


    def getMapDimensions(self):
        sumoNetfile = self.sumoNetfile
        root = ET.parse(sumoNetfile).getroot()
        for location in root.findall('location'):
            attributes = location.attrib
            sumoBBox = tuple(attributes.get('convBoundary').split(','))
            osmBBox = tuple(attributes.get('origBoundary').split(','))
            sumoBBox = tuple(float(item) for item in sumoBBox)
            osmBBox = tuple(float(item) for item in osmBBox)
            return (sumoBBox, osmBBox)


    #Translate the coordinates to distance in meters
    def translateInMeters(self,x, y):
        net = self.net
        metersDim = self.metersDim
        sumoBBox = self.sumoBBox
        (xmin,ymin,xmax,ymax) = sumoBBox
        (metersHorizontal, metersVertical) = metersDim
##        lon, lat = self.net.convertXY2LonLat(x,y)
##        print(lon+"=================="+lat)
##        return (lon, lat)
        return(x*metersHorizontal/xmax, y*metersVertical/ymax)


    
