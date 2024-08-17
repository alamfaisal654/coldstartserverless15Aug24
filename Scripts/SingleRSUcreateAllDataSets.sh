declare -a kval=("2" "4" "6" "8" "10" "12" "14" "16" "18" "20")
declare -a arrReg=("Linear" "Elastic" "XGBoost" "RandomForest" "DTR" "MLP")
for i in "${kval[@]}"
do
	echo "$i"
	python3 SingleRSUcreateDataSet.py Trainingdump.csv  SingleRSUDifferentKs "$i" 15 TrainingDataset
	python3 SingleRSUcreateDataSet.py TestingMSEdump.csv SingleRSUDifferentKs "$i" 15 TestingMSEDataset
	python3 SingleRSUcreateDataSet.py TestingRegressionDump.csv SingleRSUDifferentKs "$i" 15 TestingRegressionDataset
done

