# ================================
#   ADVANCED PYTHON TASK MANAGER
# ================================

import psutil
import subprocess
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
import time
import os


console = Console()


# ------------------------------
# SYSTEM RESOURCE FUNCTIONS
# ------------------------------
def get_cpu_usage():
    return psutil.cpu_percent(interval=0.5)


def get_memory_usage():
    mem = psutil.virtual_memory()
    return mem.used / (1024**3), mem.total / (1024**3)


def get_disks():
    disks = {}
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disks[partition.mountpoint] = (
                usage.used / (1024**3), usage.total / (1024**3)
            )
        except PermissionError:
            continue
    return disks


# ------------------------------
# PROCESS MONITORING
# ------------------------------
def get_running_processes():
    procs = []
    for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        procs.append(p.info)
    return procs


def get_top_cpu_processes(limit=10):
    processes = sorted(
        psutil.process_iter(['pid', 'name', 'cpu_percent']),
        key=lambda p: p.info['cpu_percent'],
        reverse=True
    )
    return processes[:limit]


# ------------------------------
# NETWORK STATS
# ------------------------------
def get_network_stats():
    net = psutil.net_io_counters()
    return net.bytes_sent, net.bytes_recv


# ------------------------------
# GPU USAGE (NVIDIA)
# ------------------------------
def get_gpu_usage():
    try:
        gpu = subprocess.getoutput(
            "nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits"
        )
        return f"{gpu}%"
    except Exception:
        return "No GPU / nvidia-smi not available"


# ------------------------------
# TEMPERATURES
# ------------------------------
def get_temperatures():
    try:
        temps = psutil.sensors_temperatures()
        return temps
    except:
        return {"N/A": []}


# ------------------------------
# RICH DASHBOARD DISPLAY
# ------------------------------
def build_dashboard():
    cpu = get_cpu_usage()
    mem_used, mem_total = get_memory_usage()
    disks = get_disks()
    bytes_sent, bytes_recv = get_network_stats()
    gpu = get_gpu_usage()

    # SYSTEM PANEL
    sys_panel = Panel.fit(
        f"[bold cyan]CPU:[/bold cyan] {cpu}%\n"
        f"[bold cyan]Memory:[/bold cyan] {mem_used:.2f}/{mem_total:.2f} GB\n"
        f"[bold cyan]GPU:[/bold cyan] {gpu}\n"
        f"[bold cyan]Sent:[/bold cyan] {bytes_sent/1e6:.2f} MB\n"
        f"[bold cyan]Received:[/bold cyan] {bytes_recv/1e6:.2f} MB",
        title="[bold yellow]System Usage[/bold yellow]"
    )

    # DISK TABLE
    disk_table = Table(title="Disk Usage")
    disk_table.add_column("Disk")
    disk_table.add_column("Used / Total (GB)")
    for mount, (used, total) in disks.items():
        disk_table.add_row(mount, f"{used:.2f}/{total:.2f}")

    # TOP PROCESSES
    top_table = Table(title="Top CPU Processes")
    top_table.add_column("PID")
    top_table.add_column("Name")
    top_table.add_column("CPU%")

    for proc in get_top_cpu_processes(10):
        info = proc.info
        top_table.add_row(str(info["pid"]), info["name"], str(info["cpu_percent"]))

    dashboard = Table.grid(expand=True)
    dashboard.add_row(sys_panel)
    dashboard.add_row(disk_table)
    dashboard.add_row(top_table)

    return dashboard


# ------------------------------
# MAIN LOOP
# ------------------------------
def main():
    with Live(build_dashboard(), refresh_per_second=1) as live:
        while True:
            time.sleep(1)
            live.update(build_dashboard())


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting Task Manager...")
