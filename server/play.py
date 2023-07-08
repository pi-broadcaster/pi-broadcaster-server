# Import library
import os, time, json
from datetime import datetime
# Read config.json file
f = open("config.json", "r", encoding="utf-8")
config = f.read()
config = json.loads(config)
f.close()
# Open (or try to init) cache file
max = int(config[0]["dir"])
for i in range(1, len(config)):
    if int(config[i]["dir"]) > max:
        max = int(config[i]["dir"])
try:
    cache = open("cache", "r", encoding="utf-8")
except:
    fcache = open("cache", "w", encoding="utf-8")
    for i in range(0, max):
        fcache.write("0\n")
    fcache.close()
# Read and write cache file
cache = open("cache", "r", encoding="utf-8")
index_temp = cache.readlines()
index = []
for i in range(0, len(index_temp)):
    index.append(int(index_temp[i]))
cache.close()
fcache = open("cache", "a", encoding="utf-8")
if len(index) < max:
    for i in range(0, max - len(index)):
        fcache.write("0\n")
        index.append(0)
fcache.close()
# Main
while True:
    time.sleep(0.05)
    try:
        for i in range(0, len(config)):
            id = int(config[i]["dir"]) - 1
            time.sleep(0.05)
            now = datetime.now()
            if (now.hour * 3600 + now.minute * 60 + now.second <= config[i]["time"] * 3600) and (datetime.now().weekday() in config[i]["day"]) and len(os.listdir(config[i]["dir"])) != 0:
                time.sleep(config[i]["time"] * 3600 - (now.hour * 3600 + now.minute * 60 + now.second))
                file = "\"" + str(index[i]) +".mp3\""
                index[id] += 1
                if index[id] == len(os.listdir(config[i]["dir"])) + 1 or config[i]["type"] == "text":
                    index[id] = 0
                fcache = open("cache", "w", encoding="utf-8")
                for el in index:
                    fcache.write(str(el) + "\n")
                fcache.close()
                os.chdir(config[i]["dir"])
                os.system("mpg123 " + file)
                if config[i]["type"] == "text":
                    os.system("mpg123 " + file)
                    os.system("mpg123 " + file)
                os.chdir("..")
    except:
        pass