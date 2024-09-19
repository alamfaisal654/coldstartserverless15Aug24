#declare -a lastvalarray=("2" "4" "6" "8" "10" "12" "14" "16" "18" "20")
#declare -a futurevalarray=("2" "4" "6" "8" "10" "12" "14" "16" "18" "20")
declare -a lastvalarray=("5" "10" "15")
declare -a futurevalarray=("5" "10" "15")
#declare -a arrReg=("Linear" "Elastic" "XGBoost" "RandomForest" "DTR" )
declare -a arrReg=("Elastic")
declare -a allRSUs=("1" "2" "4" "7" "11")
echo "HELLO"
precursor="SingleRSUTestingRegression"
for i in "${lastvalarray[@]}"; do
	echo "HELLO1"
	for j in "${futurevalarray[@]}"; do
		echo "HELLO2"
		# python3 SingleRSUcreateDataSet.py Trainingdump.csv  "AllDatasets/Last$i/Future$j/" "$i" "$j" "$precursor"
		# python3 SingleRSUcreateDataSet.py TestingMSEdump.csv "AllDatasets/Last$i/Future$j/" "$i" "$j" "$precursor"
		# python3 SingleRSUcreateDataSet.py TestingRegressionDump.csv "AllDatasets/Last$i/Future$j/" "$i" "$j" "$precursor"
		for k in "${arrReg[@]}"; do
			# python3 SingleRSUsaveRegressionModels.py "AllDatasets/Last$i/Future$j/" "$i" "$j" "$precursor" "$k"
			# python3 SingleRSUapplyRegressions.py "$precursor" "AllDatasets/Last$i/Future$j/" "$i" "$j" "$k"

			echo "HE"
			for m in "${allRSUs[@]}"; do
				echo "RSU=$m"
				echo "RequestGenerator.js TestingRegressionDump.csv $i $j $m $k SingleRSU 3 "
				node RequestGenerator.js TestingRegressionDump.csv "$i" "$j" "$m" "$k" SingleRSU 3
			done
		done
		# rm AllDatasets/Last"$i"/Future"$j"/"$precursor"*.csv

	done
done


# declare -a kval=("2" "4" "6" "8" "10" "12" "14" "16" "18" "20")
# declare -a arrReg=("Linear" "Elastic" "XGBoost" "RandomForest" "DTR" "MLP")
# for i in "${kval[@]}"
# do
# 	echo "$i"
# 	python3 SingleRSUcreateDataSet.py Trainingdump.csv  SingleRSUDifferentKs "$i" 15 TrainingDataset
# 	python3 SingleRSUcreateDataSet.py TestingMSEdump.csv SingleRSUDifferentKs "$i" 15 TestingMSEDataset
# 	python3 SingleRSUcreateDataSet.py TestingRegressionDump.csv SingleRSUDifferentKs "$i" 15 TestingRegressionDataset
# done

