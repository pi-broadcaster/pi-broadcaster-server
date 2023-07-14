const fs = require("fs")
const path = require("path")
const gtts = require("node-gtts")("vi")
const {execSync, spawn} = require('child_process')
const internetAvailable = require("internet-available")
/*
function internetOn() {
    let on
    internetAvailable({
        timeout: 1000,
        retries: 10,
    }).then(function(){
        on = true
    }).catch(function(){
        on = false
    })
    return on
}
*/
let play = spawn('node', ['./play.js']);

play.stdout.on('data', function (data) {
  console.log('stdout: ' + data.toString());
});

play.stderr.on('data', function (data) {
  console.log('stderr: ' + data.toString());
});

play.on('exit', function (code) {
  console.log('child process exited with code ' + code.toString());
});
let config = JSON.parse(fs.readFileSync(path.join(__dirname, "config.json"), "utf8"))

function countFolder() {
    let count = 0
    fs.readdirSync(".").forEach(item => {
        if (/^\d+$/.test(item) && fs.lstatSync(path.join(__dirname, item)).isDirectory()) count++
    })
    return count
}

for(let i = 1; i <= config.length; i++) {
    if (!fs.existsSync(path.join(__dirname, i.toString()))) {
        fs.mkdirSync(path.join(__dirname, (countFolder() + 1).toString()))
        config[i - 1].dir = countFolder()
    }
}
fs.writeFileSync(path.join(__dirname, "config.json"), JSON.stringify(config))
config = JSON.parse(fs.readFileSync(path.join(__dirname, "config.json"), "utf8"))

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
    let Path = path.join(__dirname, (i + 1).toString())
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

function generateText(a) {
    try {
        gtts.save(path.join(__dirname, a.dir.toString(), "0.mp3"), a.id, function(err) {
            if (err) { 
                console.error(err) 
                generateText(a)
            }
            console.log(`make text ok`)
        })
    } catch (err) {
        console.error(err) 
        generateText(a)
    }
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

async function getList(a) {
    let data
    await internetAvailable({
        timeout: 1000,
        retries: 10,
    }).then(function(){
        let output = execSync(`yt-dlp -j --flat-playlist ${a.id}`).toString()
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
    let command = `yt-dlp -i --extract-audio --audio-format mp3 -o "${path.join(__dirname, a.dir.toString(), `${i.toString()}.mp3`)}" https://youtube.com/watch?v=${data[i].id}`
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

async function downloadProcess(i) {
    if (config[i].type === "text") {
        console.log(`${i} make text`)
        makeText(config[i])
    } else if (config[i].type === "link") {
        console.log(`${i} get list`)
        let data = await getList(config[i])
        console.log(`${i} get list ok`)
        console.log(`${fs.readdirSync(config[i].dir.toString()).length.toString()} to ${data.length.toString()}`)
        for(let index = fs.readdirSync(config[i].dir.toString()).length; index < data.length; index++) {
            console.log(`${index} download`)
            let k = await download(config[i], index, data)
            console.log(`${index} download ok ${k}`)
        }
    }

}

for(let i = 0; i < config.length; i++) {
    console.log(`process ${i} spawned`)
    downloadProcess(i)
}
