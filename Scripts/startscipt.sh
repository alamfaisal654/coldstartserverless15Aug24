for i in {0..14}; do echo $i; node RequestGenerator.js TestingRegressionDump.csv "$i" PRED_NEW; sleep 90s; echo "===================="; done
