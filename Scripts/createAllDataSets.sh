#declare -a lastvalarray=("2" "4" "6" "8" "10" "12" "14" "16" "18" "20")
#declare -a futurevalarray=("2" "4" "6" "8" "10" "12" "14" "16" "18" "20")
declare -a lastvalarray=("6" "12" "18")
declare -a futurevalarray=("6" "12" "18")
#declare -a arrReg=("Linear" "Elastic" "XGBoost" "RandomForest" "DTR" )
declare -a arrReg=("Linear" "Elastic" "XGBoost")
echo "HELLO"
for i in "${lastvalarray[@]}"; do
	#echo "HELLO1"
	for j in "${futurevalarray[@]}"; do
		#echo "HELLO2"
		python3 createDataSet.py Trainingdump.csv AllDatasets/Last"$i"/Future"$j"/TrainingDataset.csv "$i" "$j" 
		# python3 createDataSet.py TestingMSEdump.csv AllDatasets/Last"$i"/Future"$j"/TestingMSEDataset.csv "$i" "$j"
		# python3 createDataSet.py TestingRegressionDump.csv AllDatasets/Last"$i"/Future"$j"/TestingRegressionDataset.csv "$i" "$j"
		for k in "${arrReg[@]}"; do
			python3 saveRegressionModels.py "$i" "$j" "$k"
			#echo "No step $i $j $k"
		done
		# rm AllDatasets/Last"$i"/Future"$j"/TrainingDataset.csv

	done
done
