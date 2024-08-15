#python3 createDataSet.py Trainingdump.csv DifferentKs/K600/TrainingDataset.csv 600 300

declare -a arr=("600" "540" "480" "420" "360" "300" "240" "180" "120" "60")
declare -a arrReg=("Linear" "Elastic" "XGBoost" "RandomForest" "DTR" "MLP")
for i in "${arr[@]}"
do
	for i in "${arr[@]}"
	do
		echo "$i"
		python3 createDataSet.py TestingMSE.csv DifferentKs/K"$i"/TestingMSEDataset.csv "$i" 300
		# or do whatever with individual element of the array
	done
done
