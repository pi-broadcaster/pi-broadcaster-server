# Import library
import os, json, socket, time, datetime, shutil
from urllib.request import urlopen
from gtts import gTTS
# Internet connection check
def internet_on(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        print(ex)
        return False
# Read config.json file 
f = open("config.json", "r", encoding="utf-8")
config = f.read()
config = json.loads(config)
f.close()
# Remove rubbish
for i in range(0, len(config)):
    if not os.path.isdir(config[i]["dir"]):
        os.mkdir(config[i]["dir"])
    os.chdir(config[i]["dir"])
    for item in os.listdir("."):
        if item.endswith(".webm"):
            os.remove(item.replace(".webm", ".mp3"))
            os.remove(item)
        elif item.find(".ytdl") != -1 or item.find(".part") != -1:
            os.remove(item)
        elif config[i]["type"] == "text":
            os.chdir("..")
            shutil.rmtree(config[i]["dir"])
            os.mkdir(config[i]["dir"])
            os.chdir(config[i]["dir"])
    os.chdir("..")
end = datetime.time(23, 59, 59)
# Main
while True:
    time.sleep(0.05)
    try:
        for index in range(0, len(config)):
            time.sleep(0.05)
            now = datetime.datetime.now()
            if (datetime.datetime.now().weekday() in config[index]["day"]) and (now.hour * 3600 + now.minute * 60 + now.second <= config[index]["time"] * 3600) and internet_on():
                if config[index]["type"] == "link":
                    playlist = os.popen("python3 yt-dlp -j --flat-playlist " + config[index]["id"]).read()
                    data = json.loads("[" +  playlist.replace("\n", ",")[0:len(playlist.replace("\n", ",")) - 1] + "]")
                    for i in range(len(os.listdir(config[index]["dir"])), len(data)):
                        if internet_on():
                            while True:
                                time.sleep(0.05)
                                command = "python3 yt-dlp -i --extract-audio --audio-format mp3 -o \"" + config[index]["dir"] + "/" + str(i) + ".%(ext)s\" https://youtube.com/watch?v=" + data[i]["id"]
                                print(command)
                                os.system(command)
                                if os.listdir(config[i]["dir"]).count(str(i) + ".mp3") > 0:
                                    break
                            if datetime.datetime.now().hour * 3600 + datetime.datetime.now().minute * 60 + datetime.datetime.now().second >= config[index]["time"] * 3600:
                                break
                else:
                    if internet_on() and not "ok" in os.listdir(config[index]["dir"]):
                        gTTS(config[index]["id"], lang="vi", slow=False).save(config[index]["dir"] + "/0.mp3")
                        open(config[index]["dir"] + "/ok", "w").close()
                        time.sleep(15)
    except:
        pass
