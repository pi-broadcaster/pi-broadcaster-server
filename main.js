import fs from "fs"
import path from "path"
import { Worker } from "worker_threads"

let config = JSON.parse(fs.readFileSync("config.json", "utf8"))

function countFolder() {
    let count = 0
    fs.readdirSync(".").forEach(item => {
        if (/^\d+$/.test(item) && fs.lstatSync(item).isDirectory()) count++
    })
    return count
}

for(let i = 1; i <= config.length; i++) {
    if (!config[i - 1].dir) {
        fs.mkdirSync((countFolder() + 1).toString())
        config[i - 1].dir = countFolder()
    }
}
fs.writeFileSync("config.json", JSON.stringify(config))
config = JSON.parse(fs.readFileSync("config.json", "utf8"))

function fileFilter(startPath, filter) {
    let files = fs.readdirSync(startPath)
    for (let i = 0; i < files.length; i++) {
        let filename = path.join(startPath, files[i])
        if (filename.endsWith(filter)) {
            if (filter == ".webm" && fs.existsSync(filename.replace(".webm", ".mp3"))) {
                fs.unlinkSync(filename.replace(".webm", ".mp3"))
            }
            fs.unlinkSync(filename)
        }
    }
}

for (let i = 0; i < config.length; i++) {
    let Path = (i + 1).toString()
    fileFilter(Path, '.webm')
    fileFilter(Path, '.part')
    fileFilter(Path, '.ytdl')
    if (config[i].type === "text" && fs.readdirSync(Path).length > 2) {
        let files = fs.readdirSync(Path)
        for (let i = 0; i < files.length; i++) {
            fs.unlinkSync(path.join(Path, files[i]))
        }
    }
}
console.log("filter and config ok")
new Worker('./play.js');

async function generateProcess(i) {
    if (config[i].type === "text") {
        console.log(`${i} make text`)
        let text = new Worker("./text.js")
        text.postMessage(config[i])
    } else if (config[i].type === "link") {
        console.log(`${i} download`)
        let vid = new Worker("./download.js")
        vid.postMessage(config[i])
    }

}

for(let i = 0; i < config.length; i++) {
    console.log(`process ${i} spawned`)
    generateProcess(i)
}
