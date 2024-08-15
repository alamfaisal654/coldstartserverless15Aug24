import xml.etree.ElementTree as ET
def parseRSUs():
    junctions = {}
##    RSUFile = self.RSUFile
    RSUFile = "/pvol/InTAS/scenario/selected.poly.xml"
    root = ET.parse(RSUFile).getroot()
    for poi in root.findall('poi'):
        attributes = poi.attrib
        id = attributes.get('id')
        lon = float(attributes.get('lon'))
        lat = float(attributes.get('lat'))
        junctions[id]=(lat,lon)
    return junctions
    
