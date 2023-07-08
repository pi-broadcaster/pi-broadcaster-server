import os, threading

download = threading.Thread(target=os.system, args=("python3 download.py", ))
play = threading.Thread(target=os.system, args=("python3 play.py", ))

download.start()
play.start()

download.join()
play.join()
