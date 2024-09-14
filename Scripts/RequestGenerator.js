const fs = require("fs");
//const { parse } = require("csv-parse");
//const byline = require('byline');  
//const FormData = require('form-data');
const axios = require('axios');
const { exec } = require('child_process');
const winston = require('winston');
const http = require('http')


var FILE = process.argv[2];
var LAST = process.argv[3];
var FUTURE = process.argv[4];
var RSUNum = parseInt(process.argv[5]);
var RegrType = process.argv[6];
var scalerType = process.argv[7];
var numParRequest = parseInt(process.argv[8]);



//Create Folder for Logging
var modelFolder = ""
var logFolder = ""
if (RegrType != "NONE") {
  modelFolder = "./AllDatasets/Last" + LAST + "/Future" + FUTURE + "/" + RegrType
  logFolder = modelFolder + "/" + scalerType

} else {
  modelFolder = "./AllDatasets/Last" + LAST + "/Future" + FUTURE + "/"
  logFolder = modelFolder + "/" + scalerType
}
if (!fs.existsSync(logFolder)) {
  fs.mkdirSync(logFolder);
}

previousTime = 0;
presentTime = 0;
reqid = 0;

const nReadlines = require('n-readlines');
const requestFile = new nReadlines(FILE);
jsonAutoscaleObject = {}

const loggerSuccFail = winston.createLogger({
  format: winston.format.simple(),
  transports: [
    new winston.transports.File({ filename: logFolder + '/succFail.log', options: { flags: 'w' } })
  ]
});

const logNumReplicas = winston.createLogger({
  format: winston.format.simple(),
  transports: [
    new winston.transports.File({ filename: logFolder + '/numReplicas.log', options: { flags: 'w' } })
  ]
});

const logNumReplicasError = winston.createLogger({
  format: winston.format.simple(),
  transports: [
    new winston.transports.File({ filename: logFolder + '/numReplicasError.log', options: { flags: 'w' } })
  ]
});

function parseJSONObject() {
  global.jsonAutoscaleObject = require(modelFolder+'/RSUPrediction_' + RSUNum + '.json');
}

axios.interceptors.request.use(function (config) {

  config.metadata = { startTime: new Date() }
  return config;
}, function (error) {
  return Promise.reject(error);
});

axios.interceptors.response.use(function (response) {

  response.config.metadata.endTime = new Date()
  response.duration = response.config.metadata.endTime - response.config.metadata.startTime
  return response;
}, function (error) {
  error.config.metadata.endTime = new Date();
  error.duration = error.config.metadata.endTime - error.config.metadata.startTime;
  return Promise.reject(error);
});

setInterval(function () {
  exec('kubectl get pod| grep Running| wc -l', (err, stdout, stderr) => {
    if (err) {
      // node couldn't execute the command
      return;
    }
    output = `${stdout}`;
    output = output.replace(/^\s*|\s*$/g, '');
    logNumReplicas.info(global.presentTime + "=" + output);


    output = `${stderr}`;
    output = output.replace(/^\s*|\s*$/g, '');
    logNumReplicasError.info(global.presentTime + "=" + output);

  });
}, 3000);

function autoscale() {
  console.log("Looking to autoscale")
  if (!isNaN(global.presentTime) && global.presentTime != 0) {
    console.log("autoscaling")
    projected = parseInt(global.jsonAutoscaleObject["" + global.presentTime])
    projected = projected
    console.log(global.presentTime)
    console.log(global.jsonAutoscaleObject["" + global.presentTime])
    scale = Math.floor(projected / numParRequest);
    str12 = "kubectl scale --replicas=" + scale + " deployment.apps/mydeploymentrsu" + RSUNum
    console.log(str12)

    //	  process.exit()
    exec(str12, (err, stdout, stderr) => {
      if (err) {
        // node couldn't execute the command
        return;
      }
      output = `${stdout}`;
      output = output.replace(/^\s*|\s*$/g, '');
      console.log(global.presentTime + "," + output);


      output = `${stderr}`;
      output = output.replace(/^\s*|\s*$/g, '');
      console.log(global.presentTime + "," + output);

    });
  }
}
setInterval(autoscale, parseInt(FUTURE)*1000);


setInterval(function () {
  exec('kubectl get pod| grep Running| wc -l', (err, stdout, stderr) => {
    if (err) {
      // node couldn't execute the command
      return;
    }
    output = `${stdout}`;
    output = output.replace(/^\s*|\s*$/g, '');
    logNumReplicas.info(global.presentTime + "=" + output);


    output = `${stderr}`;
    output = output.replace(/^\s*|\s*$/g, '');
    logNumReplicasError.info(global.presentTime + "=" + output);

  });
}, 2000);



setInterval(function () {

  line = requestFile.next();
  if (!line)
    process.exit();
  line = line.toString('ascii');
  linearr = line.toString().split(',');
  numRequests = linearr[RSUNum + 1];
  global.presentTime = linearr[0];
  numRequests = numRequests;
  numRequests = parseInt(numRequests, 10);

  console.log(global.presentTime + "," + numRequests);
  global.reqid = global.reqid + 1;

  //For Prediction
  for (let i = 0; i < numRequests; i++) {
    axios.get("http://192.168.49.2/rsu"+RSUNum+"q", {
      headers: {
        'Host': 'hello-world.example'
      },
      timeout: 200,
      httpAgent: new http.Agent({ keepAlive: true })
    })


      //For RPS
      /*
       
        for (let i = 0; i < numRequests; i++) {
          // console.log("hi-"+i);
          axios.get("http://192.168.58.2:32708", {
             headers: {
               'Host': 'helloworld-go.default.example.com'
             },
            timeout: 300,
          })
      
      */
      .then((response) => {
        // console.log("SUCCESS");
        loggerSuccFail.info(global.presentTime + "," + response.data + "," + response.duration);
        console.info(global.presentTime + "=" + response.data + "=" + numRequests);

      }).catch((error) => {
        // console.log("Fail");
        console.log("Error," + error);
        loggerSuccFail.info(global.presentTime + ",Fail," + error.duration);
        console.info(global.presentTime + "=Fail" + "=" + numRequests);
      });
  }
}, 1000);

parseJSONObject()
setTimeout(autoscale, 2000);




