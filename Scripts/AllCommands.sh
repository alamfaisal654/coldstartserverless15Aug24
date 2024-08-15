/usr/share/sumo/tools/randomTrips.py -n roadmesh.xml -e 5000
sumo -c simple.sumocfg  --fcd-output sumoTrace.xml
python3 createRequestDump.py ../Maps/CBD/Scale_0.1/sumoTrace.xml ../Maps/CBD/metro.net.xml ../TempFiles/reqdump.csv 2000 1000 RSU.add.xml
python3 getReqPerSec.py roadmesh.xml reqdump.csv ratedump.csv
python createDataSet.py ratedump.csv dataset.csv 10 15
python LinearRegression.py roadmesh.xml dataset.csv 10
