const fs = require("fs");
//const { parse } = require("csv-parse");
//const byline = require('byline');  
//const FormData = require('form-data');
const axios = require('axios');
const { exec } = require('child_process');
const winston = require('winston');
const http = require('http')

var FILE = process.argv[2];
var RSUNum = parseInt(process.argv[3]);
var scalerType = process.argv[4];

previousTime = 0;
presentTime =0;
reqid = 0;

const nReadlines = require('n-readlines');
const requestFile = new nReadlines(FILE);
jsonAutoscaleObject = {}

const loggerSuccFail = winston.createLogger({
  format: winston.format.simple(),
  transports: [
    new winston.transports.File({ filename: 'Output/RSU_'+RSUNum+'/'+scalerType+'/succFail.log' ,options: { flags: 'w' } })
  ]
});

const logNumReplicas = winston.createLogger({
  format: winston.format.simple(),
  transports: [
    new winston.transports.File({ filename: 'Output/RSU_'+RSUNum+'/'+scalerType+'/numReplicas.log' ,options: { flags: 'w' } })
  ]
});

const logNumReplicasError = winston.createLogger({
  format: winston.format.simple(),
  transports: [
    new winston.transports.File({ filename: 'Output/RSU_'+RSUNum+'/'+scalerType+'/numReplicasError.log' ,options: { flags: 'w' } })
  ]
});

function parseJSONObject() {
  global.jsonAutoscaleObject = require('./DifferentKs/K12/Elastic/RSUPrediction_'+RSUNum+'.json');
}

axios.interceptors.request.use(function (config) {

  config.metadata = { startTime: new Date()}
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
    logNumReplicas.info(global.presentTime+"="+output);


    output = `${stderr}`;
    output = output.replace(/^\s*|\s*$/g, '');
    logNumReplicasError.info(global.presentTime+"="+output);

  });
}, 3000);

function autoscale() {
  console.log("Looking to autoscale")
  if( !isNaN(global.presentTime) && global.presentTime!=0) {
  console.log("autoscaling")
  projected = parseInt(global.jsonAutoscaleObject[""+global.presentTime])
  projected = projected 
  console.log(global.presentTime)
  console.log(global.jsonAutoscaleObject[""+global.presentTime])
  scale = Math.floor(projected/3);
  str12 = "kubectl scale --replicas="+scale+" deployment.apps/mydeployment"

  console.log(str12)

//	  process.exit()
  exec(str12, (err, stdout, stderr) => {
    if (err) {
      // node couldn't execute the command
      return;
    }
    output = `${stdout}`;
    output = output.replace(/^\s*|\s*$/g, '');
    console.log(global.presentTime+","+output);


    output = `${stderr}`;
    output = output.replace(/^\s*|\s*$/g, '');
    console.log(global.presentTime+","+output);

  });
  }
}


setInterval(autoscale, 300000);


setInterval(function () {
  exec('kubectl get pod| grep Running| wc -l', (err, stdout, stderr) => {
    if (err) {
      // node couldn't execute the command
      return;
    }
    output = `${stdout}`;
    output = output.replace(/^\s*|\s*$/g, '');
    logNumReplicas.info(global.presentTime+"="+output);


    output = `${stderr}`;
    output = output.replace(/^\s*|\s*$/g, '');
    logNumReplicasError.info(global.presentTime+"="+output);

  });
}, 2000);



setInterval(function () {
  
  line = requestFile.next();
  if(!line)
    process.exit();
  line = line.toString('ascii');
  linearr = line.toString().split(',');
  numRequests = linearr[RSUNum+1];
  global.presentTime = linearr[0];
  numRequests = numRequests;
  numRequests = parseInt(numRequests, 10);

  console.log(global.presentTime+","+numRequests);
  global.reqid = global.reqid + 1;

//For Prediction
  for (let i = 0; i < numRequests; i++) {
    axios.get("http://192.168.58.2/hello?num="+global.reqid, {
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
        loggerSuccFail.info(global.presentTime+","+response.data+","+response.duration);
        console.info(global.presentTime+"="+response.data+"="+numRequests);
      
      }).catch((error) => {
        // console.log("Fail");
        console.log("Error,"+error);
        loggerSuccFail.info(global.presentTime+",Fail,"+error.duration);
        console.info(global.presentTime+"=Fail"+"="+numRequests);
      });
  }
}, 1000);


async function sendRequest(port) {
  try {
    var bodyFormData = new FormData();
    const image = fs.readFileSync('./abc.jpg');
    bodyFormData.append('image_file', image, 'abc.jpg');

    //const  response = await axios.post('http://127.0.0.1:'+port, bodyFormData, {
    const response = await axios.post('http://127.0.0.1:8080/function/hello-python', bodyFormData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    console.log("CORRECT");
    console.log(response);
  } catch (err) {
    console.log(JSON.stringify(err));
  }
}


function createRequests() {
  let stream = fs.createReadStream(FILE);
  stream = byline.createStream(stream);
  prevTime = 0;
  stream.on('data', (line) => {
    stream.pause();
    linearr = line.toString().split(',');
    presentTime = linearr[0];
    port = linearr[4];
    delay = presentTime - prevTime
    console.log(presentTime);
    Promise.resolve(line.toString())
      .then(sendRequest(port))
      .then(() => setTimeout(() => { stream.resume(); prevTime = presentTime }, delay));
  });
}

parseJSONObject()
setTimeout(autoscale, 2000);




