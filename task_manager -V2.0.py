# =====================
# Task Manager (Enhanced)
# =====================

import psutil
import time
import os

def get_system_resources():
    cpu_usage = psutil.cpu_percent(interval=1)

    mem = psutil.virtual_memory()
    mem_used = mem.used / (1024**3)
    mem_tot = mem.total / (1024**3)

    stats = {
        "CPU Usage" : f"{cpu_usage}%",
        "Memory Usage" : f"{mem_used:.2f} / {mem_tot:.2f} GB"
    }

    # Disk Usage
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            used_gb = usage.used / (1024**3)
            total_gb = usage.total / (1024**3)
            stats[f"Disk ({partition.mountpoint})"] = f"{used_gb:.2f} / {total_gb:.2f} GB"
        except PermissionError:
            continue

    return stats


def display_loop(refresh=1):
    """ Continuously update system stats like real Task Manager """
    while True:
        os.system("cls" if os.name == "nt" else "clear")

        print("===== SYSTEM RESOURCE MONITOR =====\n")
        stats = get_system_resources()
        for key, value in stats.items():
            print(f"{key:<20} : {value}")

        print("\nPress Ctrl+C to exit.")
        time.sleep(refresh)


if __name__ == "__main__":
    try:
        display_loop(1)
    except KeyboardInterrupt:
        print("\nExiting...")