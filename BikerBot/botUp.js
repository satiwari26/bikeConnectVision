const { Client, GatewayIntentBits, Intents } = require('discord.js');
const express = require('express');
const app = express();
require('dotenv').config();
const fs = require('fs');
const { GoogleGenerativeAI } = require("@google/generative-ai");
const genAI = new GoogleGenerativeAI(process.env.Google_Bard_API);
// const { joinVoiceChannel, createAudioResource, StreamType, createAudioPlayer, AudioPlayerStatus } = require('@discordjs/voice');

const client = new Client({ intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages] });
const discord_token = process.env.Discord_bot_API;

app.listen(3000, ()=>{
    console.log("Bot is running");
});

app.get("/", (req,res)=>{
    res.send("hello world! This is Bikers_Bot.");
})

client.on('messageCreate', async message => {
    let mainResponse = "";
    if(message.author.bot) return;  //to avoid making it respond to itself
    if( message.content !== ''){
    }   
        console.log(message.content);
        let promptVal = message.content.substring(21, message.content.length);
        let responsePrompt = "";
        if(promptVal.length > 0){   //only pass the value to bard if it's not null
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
});



async function run(prompt) {
    const model = genAI.getGenerativeModel({ model: "gemini-pro"});
    const result = await model.generateContent(prompt);
    const response = await result.response;
    const text = response.text();
    console.log(text);
    return text;
  }

//storing the information fetch from the user's HandGesture
class bikersInformation{
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

client.login(discord_token);