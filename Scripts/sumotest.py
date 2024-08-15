import sumolib

net = sumolib.net.readNet('metro.net.xml')




##x, y = net.convertLonLat2XY(1786.70, 571.32)

x, y = net.convertXY2LonLat(1786.70, 571.32)

print("%d %d" %(x,y))
