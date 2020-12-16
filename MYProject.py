from tkinter import *
import psutil as psu
from datetime import timedelta
from sys import argv
from time import time
from pprint import pprint as pp


NAME = argv[0]
print(NAME)


def systemInfo():
    info = {
        "User_Info": f"{psu.users()}",
        "up_Time": timedelta(seconds=time()-psu.boot_time()),
        "CPU_In_Use": f"{psu.cpu_percent(interval=.1)}%",
        "Time_On_CPU": timedelta(seconds=psu.cpu_times().system+psu.cpu_times().user),
        "Memory_In_Use": f"{psu.virtual_memory().percent}%",
        "Memory_Available": f"{psu.virtual_memory().available/(1024**3):,.3f} GiB",
        "Disk_In_Use": f"{psu.disk_usage('/home').percent}%",
        "Disk_Free": f"{psu.disk_usage('/').free/(1024**3):,.3f}GiB",
    }
    return "\n\n    SYSTEM INFO\n\n" +"\n".join([f"{key}: {value}" for key, value in info.items()])


def processInfo(name1):
    for proc in psu.process_iter(attrs=("name", "cmdline", "pid", "create_time", "cpu_percent", "cpu_times", "num_threads", "memory_percent")):
        cl = proc.info['cmdline']
        mem = proc.info['memory_percent']
        if name1 in proc.info['name'] and cl is not None and len(cl) > 0 and NAME in cl[-1]:
            PIDValue = proc.info["pid"]
            UpTime = timedelta(seconds=time()-proc.info["create_time"])
            CPUInUse = f"{proc.info['cpu_percent']}%"
            TimeOnCPU = timedelta(seconds=proc.info['cpu_times'].system + proc.info['cpu_times'].user),
            MemoryInUse = f"{mem:,.3f}%"
            MemoryUsage = f"{psu.virtual_memory().total*(mem/100)/(1024**3):,.3f} GiB",
            print("\n\n PROCESS INFO\n ")
            return f"PID : {PIDValue}\nup_Time : {UpTime}\nCPU_In_Use : {CPUInUse}\nTime_On_CPU : {TimeOnCPU}\nMemory_In_Use : {MemoryInUse}\nMemory_Usage : {MemoryUsage}\n"


a = systemInfo()
print(a)

print("\n")
b = processInfo("python")
print(b)

print("Top three process using CPU") 
pp([(p.pid, p.info['name'], sum(p.info['cpu_times'])) for p in sorted(psu.process_iter(['name', 'cpu_times']), key=lambda p: sum(p.info['cpu_times'][:2]))][-3:])

print("\n")
print("Process Actively running")
pp([(p.pid, p.info) for p in psu.process_iter(['name', 'status']) if p.info['status'] == psu.STATUS_RUNNING])

print("\n")

print("Process consuming more than 50 MB space of memory")
pp([(p.pid, p.info['name'], p.info['memory_info'].rss) for p in psu.process_iter(['name', 'memory_info']) if p.info['memory_info'].rss > 50 * 1024 * 1024])