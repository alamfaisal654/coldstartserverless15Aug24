declare -a kval=("2" "4" "6" "8" "10" "12" "14" "16" "18" "20")
declare -a arrReg=("Linear" "Elastic" "XGBoost" "RandomForest" "DTR" "MLP")
for i in "${kval[@]}"
do
	echo "$i"
	val=$((i*60))
	echo "$val"
	python3 createDataSet.py Trainingdump.csv DifferentKs/K"$i"/TrainingDataset.csv "$val" 900
	python3 createDataSet.py TestingMSEdump.csv DifferentKs/K"$i"/TestingMSEDataset.csv "$val" 900 
done

