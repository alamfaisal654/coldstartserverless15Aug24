const fs = require("fs");
const { parse } = require("csv-parse");
const byline = require('byline');  
const FormData = require('form-data');
const axios = require('axios');

var FILE = process.argv[2];

previousTime = 0;

async function sendRequest (port) {
	try{
			var bodyFormData = new FormData();
			const image = fs.readFileSync('./abc.jpg');
			bodyFormData.append('image_file', image, 'abc.jpg');

			//const  response = await axios.post('http://127.0.0.1:'+port, bodyFormData, {
			const  response = await axios.post('http://127.0.0.1:8080/function/hello-python', bodyFormData, {
					headers: {
						'Content-Type': 'multipart/form-data'
					}
				});
			console.log("CORRECT");
			console.log(response);

		} catch(err){
			// Send back the error message
			// console.log(`${(performance.now() - time) / 1000} seconds`);
			console.log(JSON.stringify(err));
			//res.status(500).send("TIMEOUT")	
			// console.log(`Error response took ${err.duration} milliseconds`);
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
    delay = presentTime-prevTime
    console.log(presentTime);
    Promise.resolve(line.toString())
      .then(sendRequest(port))
      .then(() => setTimeout(() => {stream.resume(); prevTime=presentTime}, delay));
  });
}



createRequests()


