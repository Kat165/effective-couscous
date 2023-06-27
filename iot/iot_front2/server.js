const cors = require('cors');
const express = require('express');
const app = express();
app.use(cors());

const bodyParser = require('body-parser');
app.use(bodyParser.json()); 

const mqtthost = 'test.mosquitto.org';
const mqttport = '1883';
const clientId = `mqtt_${Math.random().toString(16).slice(3)}`;

const httpport = 8080;

const http = require("http");
const mqtt = require('mqtt');

const mqttconnectUrl = `mqtt://${mqtthost}:${mqttport}`

const topicsToSubcribe = ['lodownik/temp', 'lodownik/ext_adc', 'lodownik/relay1'];

const mqttclient = mqtt.connect(mqttconnectUrl, {
    clientId,
    clean: true,
    connectTimeout: 4000,
    reconnectPeriod: 1000,
})

mqttclient.on('connect', () => {
    console.log('Connected')
    for(const topic of topicsToSubcribe){
      mqttclient.subscribe(topic, () => {
        console.log(`Subscribe to topic '${topic}'`)
      })}
})

var relay1 = '';
var temp = '';
var ext_adc = '';


mqttclient.on('message', (topic, payload) => {
    console.log('Received Message:', topic, payload.toString())
    if (topic == 'lodownik/temp'){
        temp = payload.toString()
    }
    else if (topic == 'lodownik/ext_adc'){
        ext_adc = payload.toString();
    }
    else if (topic == 'lodownik/relay1'){
        relay1 = payload.toString();
    }
})

app.post('/setpoint', (req, res) => {res.send(setpoint(req.body.temp))})
app.post('/relay0', (req, res) => {res.send(relay0(req.body.status))})
app.get('/sleep', (req, res) => {res.send(sleep())})
app.get('/reset', (req, res) => {res.send(reset())})
app.get('/ota', (req, res) => {res.send(ota())})

app.get('/relay1', (req, res) => {res.send(relay1)})
app.get('/ext_adc', (req, res) => {res.send(ext_adc)})
app.get('/temp', (req, res) => {res.send(temp)})

app.listen(httpport, () => {console.log('listening...')})

function setpoint(temperature) {
    temperature = Math.round(temperature)
    temperature = temperature.toString();
    while(temperature.length < 3){
        temperature = '0'.concat(temperature);
    }
    if(temperature.length > 3){
        temperature = temperature.slice(0, 3);
    }
    mqttclient.publish('lodownik/setpoint', temperature.toString(), {qos: 0, retain: false}, (error) => {
        if (error) {
            return error
        }
        else{
            return 'OK'
        }
    })
}

function relay0(status) {
    mqttclient.publish('lodownik/relay0', status, {qos: 0, retain: false}, (error) => {
        if (error) {
            return error
        }
        else{
            return 'OK'
        }
    })
}

function sleep() {
    mqttclient.publish('lodownik/system/sleep', '', {qos: 0, retain: false}, (error) => {
        if (error) {
            return error
        }
        else{
            return 'OK'
        }
    })
}

function reset() {
    mqttclient.publish('lodownik/system/reset', '', {qos: 0, retain: false}, (error) => {
        if (error) {
            return error
        }
        else{
            return 'OK'
        }
    })
}

function ota() {
    mqttclient.publish('lodownik/system/ota', '', {qos: 0, retain: false}, (error) => {
        if (error) {
            return error
        }
        else{
            return 'OK'
        }
    })
}

