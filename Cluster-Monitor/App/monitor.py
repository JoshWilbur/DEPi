import platform
import psutil
import socket
import datetime

def get_system_info():
    sys_info = {
        "OS": platform.system(),
        "OS Release": platform.release(),
        "Architecture": platform.architecture()[0],
        "Machine": platform.machine(),
        "Processor": platform.processor(),
        "CPU Cores (Logical)": float(psutil.cpu_count(logical=True)),
        "CPU Cores (Physical)": float(psutil.cpu_count(logical=False)),
        "RAM Total Gb": round(psutil.virtual_memory().total / (1024**3), 2),
        "Python Version": platform.python_version(),
        "Platform": platform.platform(),
        "Node": platform.node(),
        "Boot Time": datetime.datetime.fromtimestamp(psutil.boot_time()).isoformat(),
    }
    return sys_info

def get_runtime_metrics():
    vm = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    net_io = psutil.net_io_counters()
    return {
        "Cpu Percent": round(psutil.cpu_percent(interval=0.1), 2),
        "Disk Free": round(disk.free / (1024**3), 2),  # GB
        "Disk Percent": round(disk.percent, 2),
        "Disk Total": round(disk.total / (1024**3), 2),  # GB
        "Disk Used": round(disk.used / (1024**3), 2),  # GB
        "Memory Active": round(getattr(vm, "active", 0) / (1024**3), 2),
        "Memory Available": round(vm.available / (1024**3), 2),
        "Memory Buffers": round(getattr(vm, "buffers", 0) / (1024**3), 2),
        "Memory Cached": round(getattr(vm, "cached", 0) / (1024**3), 2),
        "Memory Free": round(vm.free / (1024**3), 2),
        "Memory Inactive": round(getattr(vm, "inactive", 0) / (1024**3), 2),
        "Memory Percent": round(vm.percent, 2),
        "Memory Shared": round(getattr(vm, "shared", 0) / (1024**3), 2),
        "Memory Slab": round(getattr(vm, "slab", 0) / (1024**3), 2),
        "Memory Total": round(vm.total / (1024**3), 2),
        "Memory Used": round(vm.used / (1024**3), 2),
        "Net Io Bytes Recv": round(net_io.bytes_recv / 1024, 2),  # KB
        "Net Io Bytes Sent": round(net_io.bytes_sent / 1024, 2),  # KB
        "Net Io Dropin": net_io.dropin if hasattr(net_io, "dropin") else 0,
        "Net Io Dropout": net_io.dropout if hasattr(net_io, "dropout") else 0,
        "Net Io Errin": net_io.errin if hasattr(net_io, "errin") else 0,
        "Net Io Errout": net_io.errout if hasattr(net_io, "errout") else 0,
        "Net Io Packets Recv": net_io.packets_recv,
        "Net Io Packets Sent": net_io.packets_sent,
    }

def get_network_info():
    return {
        "Hostname": socket.gethostname(),
        "Ip Address": socket.gethostbyname(socket.gethostname())
    }

def get_uptime():
    uptime_seconds = int(psutil.boot_time() - psutil.boot_time() + psutil.time.time() - psutil.boot_time())
    # Or simpler:
    uptime_seconds = int(datetime.datetime.now().timestamp() - psutil.boot_time())
    days, remainder = divmod(uptime_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{days}d {hours}h {minutes}m {seconds}s"

def get_all_metrics():
    return {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "system_info": get_system_info(),
        "runtime_metrics": get_runtime_metrics(),
        "network_info": get_network_info(),
        "uptime": get_uptime(),
    }

if __name__ == "__main__":
    import json
    print(json.dumps(get_all_metrics(), indent=2))
