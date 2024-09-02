declare -a lastvalarray=("2" "4" "6" "8" "10" "12" "14" "16" "18" "20")
declare -a futurevalarray=("2" "4" "6" "8" "10" "12" "14" "16" "18" "20")
echo "HELLO"
for i in "${lastvalarray[@]}"; do
	echo "HELLO1"
	for j in "${futurevalarray[@]}"; do
		echo "HELLO2"
		echo "$i"
		last=$((i * 60))
		future=$((j * 60))
		echo "$val"
		python3 createDataSet.py Trainingdump.csv AllDatasets/Last"$i"/Future"$j"/TrainingDataset.csv "$last" "$future"
		python3 createDataSet.py TestingMSEdump.csv AllDatasets/Last"$i"/Future"$j"/TestingMSEDataset.csv "$last" "$future"
		python3 createDataSet.py TestingRegressionDump.csv AllDatasets/Last"$i"/Future"$j"/TestingRegressionDataset.csv "$last" "$future"
	done
done
