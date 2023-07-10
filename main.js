const fs = require("fs")
const path = require("path")
const gTTs = require("gtts")
const {exec} = require('child_process');

let config = JSON.parse(fs.readFileSync(path.join(__dirname, "config.json"), "utf8"))

for(let i = 1; i <= config.length; i++) {
    if (!fs.existsSync(path.join(__dirname, i.toString()))) {
        fs.mkdirSync(path.join(__dirname, i.toString()))
    }
}

function fileFilter(startPath, filter) {
    let files = fs.readdirSync(startPath);
    for (let i = 0; i < files.length; i++) {
        let filename = path.join(startPath, files[i]);
        if (filename.endsWith(filter)) {
            fs.unlinkSync(filename);
        };
    };
};

for (let i = 0; i < config.length; i++) {
    let Path = path.join(__dirname, (i + 1).toString())
    fileFilter(Path, '.webm');
    fileFilter(Path, '.part');
    fileFilter(Path, '.ytdl');
    if (config[i].type === "text" && fs.readdirSync(Path).length > 2) {
        let files = fs.readdirSync(Path);
        for (let i = 0; i < files.length; i++) {
            fs.unlinkSync(path.join(Path, files[i]));
        };
    }
}

async function downloadProcess(i) {
    if (config[i].type === "text") {
        let gtts = new gTTS(config[i].id, 'vi')
        gtts.save('0.mp3', function (err, result) {
            if (err) { throw new Error(err) }
        })
    } else if (config[i].type === "link") {
        let data
        exec(`yt-dlp -j --flat-playlist ${config[i].id}`, (err, output) => {
            if (err) {
                console.error("could not execute command: ", err)
                return
            }
            data = JSON.parse(`[${output.replace("/\n/g", ",").substr(0, output.length - 1)}]`)
        })
        
    }

}

for(let i = 0; i < config.length; i++) {
    downloadProcess(i)
}




