const { Client, GatewayIntentBits, Intents } = require('discord.js');
const express = require('express');
const app = express();
require('dotenv').config();
const fs = require('fs');
const { GoogleGenerativeAI } = require("@google/generative-ai");
const genAI = new GoogleGenerativeAI(process.env.Google_Bard_API);
const axios = require('axios');
// const { joinVoiceChannel, createAudioResource, StreamType, createAudioPlayer, AudioPlayerStatus } = require('@discordjs/voice');

const client = new Client({ intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages] });
const discord_token = process.env.Discord_bot_API;

app.listen(3300, ()=>{
    console.log("Bot is running");
});

//storing the information fetch from the user's HandGesture
class BikersInformation{
    constructor(){  //creates the fields to store the information
        this.userUpdateData = [];
        this.status = false;
    }
    fetchInfo(){
        //fetches the information from the json file after it has been updated
        try{
            this.userUpdateData = JSON.parse(fs.readFileSync('../handGesture/data.json'));
            this.status = true;
            // console.log(this.userUpdateData);
        }
        catch(error){
            console.log(error);
            this.status = false;
        }
    }
}

async function getLocation(lat, long) {
    let response;
    if(lat == 0 && long == 0){  //base condition to exit the function
        return "No location found";
    }

    try{
        response = await axios.get(`http://dev.virtualearth.net/REST/v1/Locations/${lat},${long}?o=json&key=${process.env.Bing_Map_API}`);
    }
    catch(error){
        console.log(error);
    }
    let results;
    try{
        results = response.data.resourceSets[0].resources;
    }
    catch(error){
        console.log(error);
    }

    if (results[0]) {
        return results[0].address.formattedAddress;
    } else {
        return 'No results found';
    }
}

async function getParseData(){
    // parsing the location data for the user to get the message update
    let parseData = [];
    let bikersInformation = new BikersInformation();
    bikersInformation.fetchInfo();

    if(bikersInformation.status == true){
        let locationCoordinates = [];
        for(let i = 0; i < bikersInformation.userUpdateData.length; i++){
            locationCoordinates.push({reason: bikersInformation.userUpdateData[i].reason, location: bikersInformation.userUpdateData[i].location});

            let addr = await getLocation(bikersInformation.userUpdateData[i].location.lat,
                bikersInformation.userUpdateData[i].location.long);

            if(addr !== "No location found"){
                parseData.push({date: bikersInformation.userUpdateData[i].date,reason: bikersInformation.userUpdateData[i].reason,
                    name: bikersInformation.userUpdateData[i].userName, location: addr, 
                    time: bikersInformation.userUpdateData[i].time});
            }
        }
        app.get("/UpdateInfo", (req,res)=>{
            res.send(locationCoordinates);
        });
    }
    else{
        app.get("/UpdateInfo", (req,res)=>{
            res.send(locationCoordinates.push({lat:0,long:0}));
        });
    }
    return parseData;
}

client.on('messageCreate', async message => {
    //getting the prominant string ready for LLM
    let parseData = await getParseData();
    let prominantString = "";
    prominantString = "Can you help me write so people can understand better what is happening. These are the updates information provided by a user to another user. \n";
    for(let i = 0; i < parseData.length; i++){
        prominantString += `**Date Posted**:  ${parseData[i].date},  **Update reason**:   ${parseData[i].reason},   **User's Name**:   ${parseData[i].name},   **location**:   ${parseData[i].location},   **Time Posted**:   ${parseData[i].time} \n`;
    }

    let mainResponse = "";
    if(message.author.bot) return;  //to avoid making it respond to itself
    if( message.content !== ''){
    }   
        console.log(message.content);
        let promptVal = message.content.substring(21, message.content.length);
        if(promptVal.toLowerCase().includes("update")){ //updated string request from the user
            if(prominantString.length > 0){
                responsePrompt = await run(prominantString);
                if(responsePrompt == undefined){
                    mainResponse = "Sorry something went wrong!";
                }
                if(responsePrompt.length > 1500){
                    for(let i = 0; i < responsePrompt.length; i+=1500){
                        mainResponse = responsePrompt.substring(i, Math.min(i+1500,responsePrompt.length));
                        message.reply(mainResponse);
                    }
                }
                else if(responsePrompt !== ""){
                    try{
                        message.reply(responsePrompt);
                    }
                    catch(error){
                        console.log(error);
                        message.reply("Sorry something went wrong!");
                    }
                }
                else{
                    message.reply("Sorry something went wrong!");
                }
            }
            else{
                message.reply("No updates found at this moment!");
            }
        }
        else{   //other information request from the user
            let responsePrompt = "";
            if(promptVal.length > 0){   //only pass the value to bard if it's not null
                console.log(prominantString);
                responsePrompt = await run(promptVal);
            }
            if(responsePrompt == undefined){
                mainResponse = "Sorry something went wrong!";
            }
            if(responsePrompt.length > 1500){
                for(let i = 0; i < responsePrompt.length; i+=1500){
                    mainResponse = responsePrompt.substring(i, Math.min(i+1500,responsePrompt.length));
                    message.reply(mainResponse);
                }
            }
            else if(responsePrompt !== ""){
                try{
                    message.reply(responsePrompt);
                }
                catch(error){
                    console.log(error);
                    message.reply("Sorry something went wrong!");
                }
            }
            else{
                message.reply("Sorry something went wrong!");
            }
        }
});



async function run(prompt) {
    const model = genAI.getGenerativeModel({ model: "gemini-pro"});
    const result = await model.generateContent(prompt);
    const response = await result.response;
    const text = response.text();
    console.log(text);
    return text;
  }

client.login(discord_token);