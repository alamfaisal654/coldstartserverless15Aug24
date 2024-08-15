const express = require('express');
const path = require('path');
const app = express();
const axios = require('axios');
var multer = require('multer');
var upload = multer();
const process = require('process')
const fs = require('fs');
const FormData = require('form-data');
const execSync = require("child_process").execSync;
const { performance } = require('perf_hooks');
axios.defaults.timeout = 2000;

// for parsing application/json
app.use(express.json());

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



var PORT = process.argv[2];
var dockerNumber = 0;
var MAXINSTANCES = 10; //Maximum number of instances that can run simultaneously
console.log(PORT);

// for parsing application/x-www-form-urlencoded
 app.use(express.urlencoded({ extended: true })); 

// for parsing multipart/form-data
app.use(upload.any()); 
app.use(express.static('public'));

numRequests = 0;
numSuccesfuls = 0;
metricData = [];

// Application servers
const servers = []

// Track the current application server to send request
let current = 0;

// Receive new request
// Forward to application server
const handler = async (req, res) =>{
	//const image = fs.readFileSync('./abc.jpg');
	console.log("===========");

	// Destructure following properties from request object
	const { method, url, headers, body } = req;

	// Select the current server to forward the request
	const server = servers[current];

	// Update track to select next server
	current === (servers.length-1)? current = 0 : current++
	var bodyFormData = new FormData();
	const file = req.files[0];
	bodyFormData.append('image_file', file.buffer, file.originalname);
//	bodyFormData.append('image_file', image, 'abc.jpg');


	try{
		// Requesting to underlying application server
//		const response = await axios({
//			url: `${server}${url}`,
//			method: method,
//			headers: headers,
//			data: bodyFormData
//		});

 
		// const { response , durationInMs } = await axios.post('http://172.17.0.2:8080', bodyFormData, {
		// 	headers: {
		// 		'Content-Type': 'multipart/form-data'
		// 	}
		// });

		// console.log(headers)
		let time = performance.now();
		
		h = JSON.stringify(headers);
		numRequests++;
		const response  = await axios.post('http://172.17.0.2:8080', bodyFormData, {
			headers: h
		});
		numSuccesfuls++;
		// console.log(`${(performance.now() - time) } seconds`);
		
		// console.log("111111111111111111")
		// console.log('Response received');
		// Send back the response data
		// from application server to client
		// console.log("2222222222222222222")
		console.log(JSON.stringify(response.data));
		// console.log("33333333333333");
		res.send(JSON.stringify(response.data))
		// console.log("4444444444444444444")
		// console.log(`Successful response took ${response.duration} milliseconds`);
	}
	catch(err){
		// Send back the error message
		// console.log(`${(performance.now() - time) / 1000} seconds`);
		console.log(JSON.stringify(err));
		res.status(500).send("TIMEOUT")	
		// console.log(`Error response took ${err.duration} milliseconds`);
	}
}

function addMetricData() {
	numServers = servers.length;
	presentreq = {'numRequests':numRequests,'numSuccesfuls':numSuccesfuls, 'numServers':numServers};
	metricData.push(presentreq);
	numRequests = 0;
	numSuccesfuls = 0;
	if (metricData.length > 15) {
		metricData.splice(0,1);
	}
	// console.log('Present Data=' +JSON.stringify(metricData));
}

setInterval(addMetricData,1000);


app.get('/getmetric', function(req, res){
	res.send(JSON.stringify(metricData));
	// metricData = [];

});


function deleteInstances(num) {
	num=Math.abs(num);
	while(servers.length>0) {
		--num;
		console.log("num="+num);
		if (num<0) break;
		tup = servers[0];
		name = tup.name
		servers.splice(0,1);
		cmd = "sudo docker stop "+name+"; sudo docker rm "+name+";";
		stdout = execSync(cmd, { encoding: 'utf8', maxBuffer: 50 * 1024 * 1024 }).toString();
		stdout = stdout.trim();
		console.log(servers);
  }
}

app.get('/add', function(req, res){
	toSetInstances = req.query.num;
	presInstances = servers.length;
	addInstances(toSetInstances-presInstances, res);
});

function addInstances(num, res) {
	numIter = Math.min(num, MAXINSTANCES-servers.length)
	if(num <0) {
		deleteInstances(num);
		res.send("Deleted\n");
		return;
	}
	for (let i=0;i<numIter;i++) {
		++dockerNumber
		name = 'A_'+dockerNumber;
		if(servers.length < MAXINSTANCES) {
		// cmd = "echo ubuntu22| sudo docker run -d --name "+name+"  normchenjk/yolo-image 1>/dev/null; sudo docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' "+name+"| tr '\n' ','; echo "+name+" | tr '\n' ' '";
		   cmd = "echo ubuntu22| sudo docker run -d --name "+name+"  faisalyolo 1>/dev/null; sudo docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' "+name+"| tr '\n' ','; echo "+name+" | tr '\n' ' '";
		console.log(cmd);
		stdout = execSync(cmd, { encoding: 'utf8', maxBuffer: 50 * 1024 * 1024 }).toString();
			console.log(stdout);
			stdout = stdout.trim();
			console.log(`stdout: ${stdout}`);
			ip = stdout.split(',')[0];
			sname = stdout.split(',')[1];
			newServer = {'ip':ip,'name':sname};
			servers.push(newServer);
		} else {
			console.log("MAXIMUM INSTANCES ACHIEVED");
			res.send('MAXIMUM INSTANCES REACHED');
			return;
		}
	} 
	res.send('num: ' + numIter);
}



// Serve favicon.ico image
app.get('/', (req, res
	) => res.sendFile('/abc.jpg'));


// When receive new request
// Pass it to handler method
app.use((req,res)=>{handler(req, res)});

// Listen on PORT 8080
app.listen(PORT, err =>{
	err ?
	console.log("Failed to listen on PORT "+PORT):
	console.log("Load Balancer Server "
		+ "listening on PORT 8080");
});

