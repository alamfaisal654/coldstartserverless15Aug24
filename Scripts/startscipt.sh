for i in {0..14}; do echo $i; node RequestGenerator.js TestingRegressionDump.csv "$i" PRED_NEW| tee temp2; sleep 90s; echo "===================="; done
