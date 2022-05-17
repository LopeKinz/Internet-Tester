from addons import speedtest
import math
import time
import datetime
from pylive import live_plotter
import numpy as np
x = 100
size = x
x_vec = np.arange(0, size, 1)
y_vec = np.zeros(x)
line1 = []


def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s" % (s)


servers = []
# If you want to test against a specific server
# servers = [1234]

threads = 100
# If you want to use a single threaded test
# threads = 1
while True:
    try:
        s = speedtest.Speedtest()
        s.get_servers(servers)
        s.get_best_server()
        s.download(threads=threads)
        s.upload(threads=threads)
        s.results.share()
        results_dict = s.results.dict()
        download_speed = results_dict['download']
        upload_speed = results_dict['upload']
        ping = results_dict['ping']
        mbs_download = convert_size(download_speed)
        mbs_upload = convert_size(upload_speed)
        x = int(x) + 1
        f = (f"Download : {mbs_download} | Upload : {mbs_upload} | Ping : {ping}")
        print(f)
        file = open("speeds.txt", "a")
        file.write(f"{datetime.datetime.now()} : {f}\n")
        file.close()
        y_vec[-1] = mbs_download
        line1 = live_plotter(x_vec,y_vec,line1)
        y_vec = np.append(y_vec[1:],0.0)
    except Exception as e:
        print(e)
        f = open("errors.txt","a")
        f.write(f"{datetime.datetime.now()} : {e}\n")
        f.close()
        mbs_download = 0
        x = int(x) + 1
        y_vec[-1] = mbs_download
        line1 = live_plotter(x_vec,y_vec,line1)
        y_vec = np.append(y_vec[1:],0.0)