
declare -a arr=("2" "4" "6" "8" "10" "12" "14" "16" "18" "20")
declare -a arrReg=("Linear" "Elastic" "XGBoost" "RandomForest" "DTR" )
for j in "${arrReg[@]}"
do
	for i in "${arr[@]}"
	do
		echo "$i"
		python3 saveRegressionModels.py "$i" "$j"
	done
done
