const express = require('express');
const bodyParser = require('body-parser');
const {
    spawn
} = require('child_process');
var utf8 = require('utf8');
const path = require('path');
var fs = require('fs');
var http = require('http');
var https = require('https');
var privateKey = fs.readFileSync('node_modules/browser-sync/certs/server.key', 'utf8');
var certificate = fs.readFileSync('node_modules/browser-sync/certs/server.crt', 'utf8');
var credentials = {
    key: privateKey,
    cert: certificate
};

const app = express();
app.use(express.static(__dirname));

app.use(bodyParser.json()); // support json encoded bodies
// app.use(bodyParser.urlencoded({ extended: true })); // support encoded bodies

// Add headers
app.use(function(req, res, next) {

    // Website you wish to allow to connect
    res.setHeader('Access-Control-Allow-Origin', 'https://localhost:4200');

    // Request methods you wish to allow
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, PATCH, DELETE');

    // Request headers you wish to allow
    res.setHeader('Access-Control-Allow-Headers', 'X-Requested-With,content-type');

    // Set to true if you need the website to include cookies in the requests sent
    // to the API (e.g. in case you use sessions)
    res.setHeader('Access-Control-Allow-Credentials', true);

    // Pass to next layer of middleware
    next();
});

var httpsServer = https.createServer(credentials, app);

// some data for the API
var foods = [{
        "id": 1,
        "name": "Donuerts"
    },
    {
        "id": 2,
        "name": "Pizza"
    },
    {
        "id": 3,
        "name": "Tacos"
    }
];
// the GET "foods" API endpoint
// the GET "foods" API endpoint
app.get('/api/food', function(req, res) {

    console.log("GET foods");

    // This is a very simple API endpoint. It returns the current value of the "foods" array.
    //res.send(foods);
    var dataToSend;
    // spawn new child process to call the python script
    const python = spawn('python', ['ForeignWordsAnalytics/venv/main.py']);
    // collect data from script
    python.stdout.on('data', function(data) {
        // console.log(data);
        dataToSend = data.toString();
        console.log("dataToSend");
        console.log(dataToSend);
        console.log('asd');
    });
    // in close event we are sure that stream from child process is closed
    python.on('close', (code) => {
        console.log(`child process close all stdio with code ${code}`);
        // send data to browser
        res.send(dataToSend)
    });

});

app.get('/api/process:text', function(req, res) {

  var path = require('path');

  console.log("GET words");

  // This is a very simple API endpoint. It returns the current value of the "foods" array.
  //res.send(foods);
  var dataToSend;
  var result = "";

  // read the ID from the query string
  let text = req.params.text;
//   console.log(text);

  // spawn new child process to call the python script
  const python = spawn('python', ['ForeignWordsAnalytics/venv/main.py', text]);
//   python.stdout.setEncoding('utf8');
//   console.log(text);
  // collect data from script
  python.stdout.on('data', function(data) {
    dataToSend = data.toString();
    dataToSend = dataToSend.replace('[','').replace(']','');
    dataToSend = dataToSend.split(',');
    for (chars of dataToSend) {  
        result = result + String.fromCharCode(chars);
      };
    //   console.log(dataToSend);
    console.log(result.replace('&', '\n'));
    //   console.log(dataToSend.toString('utf8'));
    //   console.log('asd');
  });
  // in close event we are sure that stream from child process is closed
  python.on('close', (code) => {
      console.log(`child process close all stdio with code ${code}`);
      // send data to browser
      res.send(result.split('&'))
  });

});

// catch 404 and forward to error handler
// app.use(function(req, res, next) {
//     let err = new Error('Not Found');
//     err.status = 404;
//     next(err);
// });

// HTTP listener
// app.listen(4200, function () {
//     console.log('Example listening on port 3000!');
// });

httpsServer.listen(3000);
console.log('Example listening on port 3000!');

module.exports = app;
