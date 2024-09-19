declare -a lastfutvalarray=("6" "12" "18")
for i in "${lastfutvalarray[@]}"; do
    for m in {0..14}; do
        echo "RSU=$m"
        echo "Last and Future= $i"
        echo "node RequestGenerator.js TestingRegressionDump.csv $i $i $m Elastic SingleRSU 1"
        node RequestGenerator.js TestingRegressionDump.csv "$i" "$i" "$m" "Elastic" SingleRSU 1
        kubectl delete -f NoScaleService/createDeployment.yaml
        kubectl apply -f NoScaleService/createDeployment.yaml
    done
done