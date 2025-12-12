# =============
# Task Manager
# =============

import psutil

def get_system_resources():
    cpu_usage = psutil.cpu_percent(interval=1)
    
    mem = psutil.virtual_memory()
    mem_used = mem.used / (1024**3)
    mem_tot = mem.total / (1024**3)
    
    stats = {
        "CPU" : f"{cpu_usage}%",
        "Memory" : f"{mem_used:.2f} / {mem_tot:.2f} GB"
    }
    
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            used_gb = usage.used / (1024**3)
            total_gb = usage.total / (1024**3)
            stats[f"Disk ({partition.mountpoint})"] = (f"{used_gb : .2f} / {total_gb:.2f} GB")
        except PermissionError:
            continue
    
    return stats

resource = get_system_resources()
for name,usage in resource.items():
    
    print(f"{name} : {usage}")


