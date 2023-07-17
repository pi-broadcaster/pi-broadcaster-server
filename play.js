import fs from "fs"
import path from "path"
import { execSync } from "child_process"

let config = JSON.parse(fs.readFileSync("config.json", "utf8"))
function play(i) {
    if (config[i].type === "text") {
        for (let index = 0; index < 3; index++) {
            execSync(` mpg123 ${path.join(config[i].dir.toString(), "0.mp3")}`)
        }
    } else if (config[i].type === "link") {
        execSync(` mpg123 ${path.join(config[i].dir.toString(), `${config[i].index}.mp3`)}`)
        config[i].index += 1
        let count = 0
        fs.readdirSync(config[i].dir.toString()).forEach(item => {
            if (item.endsWith(".mp3")) count += 1
        })
        if (config[i].index === count) config[i].index = 0
        fs.writeFileSync("config.json", JSON.stringify(config))
        config = JSON.parse(fs.readFileSync("config.json", "utf8"))
    }
}

function playProcess(time, day, i) {
    let d = new Date()
    let sec = d.getHours() * 3600 + d.getMinutes() * 60 + d.getSeconds()
    let endDay = 24 * 3600
    let delay
    if (time >= sec) delay = (time - sec) * 1000; else delay = (endDay - sec + time) * 1000
    console.log(`set delay ${delay}`)
    console.log(`play process ${i}`)
    console.log(`play at ${(Math.floor(delay / 3600000)).toString()}:${(Math.floor(((delay / 3600000) * 60) % 60)).toString()}`)
    setTimeout(() => {
        let wd = new Date()
        let wday = (wd.getDay() == 0 ? 7 : wd.getDay()) - 1
        console.log("play")
        if (day.includes(wday)) {
            play(i)
            console.log("play ok")
        }
        console.log("play fin")
        playProcess(time, day, i)
    }, delay)
}

for(let i = 0; i < config.length; i++) {
    config[i].tm.forEach(tm => playProcess(tm.time * 3600, tm.day, i))
}




