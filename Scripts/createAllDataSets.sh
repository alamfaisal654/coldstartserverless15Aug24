#declare -a lastvalarray=("2" "4" "6" "8" "10" "12" "14" "16" "18" "20")
#declare -a futurevalarray=("2" "4" "6" "8" "10" "12" "14" "16" "18" "20")
declare -a lastvalarray=("5" "15")
declare -a futurevalarray=("5" "15")
#declare -a arrReg=("Linear" "Elastic" "XGBoost" "RandomForest" "DTR" )
declare -a arrReg=("Elastic")
declare -a allRSUs=("1" "2" "4" "7" "11")
echo "HELLO"
for i in "${lastvalarray[@]}"; do
	#echo "HELLO1"
	for j in "${futurevalarray[@]}"; do
		#echo "HELLO2"
		# python3 createDataSet.py Trainingdump.csv AllDatasets/Last"$i"/Future"$j"/TrainingDataset.csv "$i" "$j" 
		# python3 createDataSet.py TestingMSEdump.csv AllDatasets/Last"$i"/Future"$j"/TestingMSEDataset.csv "$i" "$j"
		# python3 createDataSet.py TestingRegressionDump.csv AllDatasets/Last"$i"/Future"$j"/TestingRegressionDataset.csv "$i" "$j"
		for k in "${arrReg[@]}"; do
			# python3 saveRegressionModels.py "$i" "$j" "$k"
			# python3 applyRegressionModels.py "TestingMSEDataset.csv" "$i" "$j" "$k"
			#echo "No step $i $j $k"

			# echo "HE"
			for m in "${allRSUs[@]}"; do
				echo "RSU=$m"
				kubectl delete -f NoScaleService/createDeployment.yaml 
				kubectl apply -f NoScaleService/createDeployment.yaml 
				echo "node RequestGenerator.js TestingRegressionDump.csv $i $j $m $k AllRSU 5"
				node RequestGenerator.js TestingRegressionDump.csv "$i" "$j" "$m" "$k" AllRSU 5
			done
			# sleep 70m
		done
		# rm AllDatasets/Last"$i"/Future"$j"/TrainingDataset.csv
	done
done
