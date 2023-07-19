import fs from "fs"
import path from "path"
import { parentPort } from "worker_threads"
import {execSync} from "child_process"
import internetAvailable from "internet-available"

async function getList(a) {
    let data
    await internetAvailable({
        timeout: 1000,
        retries: 10,
    }).then(function(){
        let output = execSync(` yt-dlp -j --flat-playlist ${a.id} --playlist-reverse`).toString()
        data = JSON.parse(`[${output.replace(/\n/g, ",").substr(0, output.length - 1)}]`)
    }).catch(async function(err){
        console.error(err)
        console.log(`get list -ing`)
        data = await getList(a)
    })
    return data
}

async function download(a, i, data) {
    let k
    let command = ` yt-dlp -i --force-overwrites --extract-audio --audio-format mp3 -o "${path.join(a.dir.toString(), `${i.toString()}.mp3`)}" https://youtube.com/watch?v=${data[i].id}`
    await internetAvailable({
        timeout: 1000,
        retries: 10,
    }).then(function(){
        console.log(command)
        execSync(command)
        k = 0
    }).catch(async function(err){
        console.error(err)
        console.log("oops")
        k = await download(a, i, data)
    })
    return k
}

async function downloadP(a) {
    console.log(`get list`)
    let data = await getList(a)
    console.log(`get list ok`)
    console.log(`${fs.readdirSync(a.dir.toString()).length.toString()} to ${data.length.toString()}`)
    for(let index = fs.readdirSync(a.dir.toString()).length; index < data.length; index++) {
        console.log(`${index} download`)
        let k = await download(a, index, data)
        console.log(`${index} download ok ${k}`)
    }
}

parentPort.once("message", a => {
    downloadP(a)
})