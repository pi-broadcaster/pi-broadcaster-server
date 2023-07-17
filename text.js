import { parentPort } from "worker_threads"
import {execSync} from "child_process"
import internetAvailable from "internet-available"

function generateText(a) {
    console.log("start make text")
    execSync(`gtts-cli "${a.id}" -l vi -o ${a.dir.toString()}/0.mp3`)
    console.log("make text ok")
}

function makeText(a) {
    internetAvailable({
        timeout: 1000,
        retries: 10,
    }).then(function(){
        generateText(a)
    }).catch(function(err){
        console.error(err)
        makeText(a)
    })
}
parentPort.once("message", a => {
    makeText(a)
})
