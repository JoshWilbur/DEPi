import platform
import psutil
import socket
import datetime
import time

def get_system_info():
    sys_info = {
        "OS": platform.system(),
        "OS Release": platform.release(),
        "Architecture": platform.architecture()[0],
        "Machine": platform.machine(),
        "CPU Cores (Physical)": psutil.cpu_count(logical=False),
        "CPU Cores (Logical)": psutil.cpu_count(logical=True),
        "Python Version": platform.python_version(),
        "Boot Time": datetime.datetime.fromtimestamp(psutil.boot_time()).isoformat(),
    }
    return sys_info

def get_temperature_info():
    temps = psutil.sensors_temperatures()
    # temps is a dict: keys = sensor label, values = list of temperature objects with current temp
    temperature_data = {}
    for name, entries in temps.items():
        # Aggregate temps by sensor type, average them or take max
        # For simplicity take max current temp in each sensor group
        max_temp = max(entry.current for entry in entries if entry.current is not None)
        temperature_data[name] = round(max_temp, 1)
    return temperature_data

def get_runtime_metrics():
    vm = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    return {
        "Cpu Percent": round(psutil.cpu_percent(interval=0.1), 2),
        "Disk Percent": round(disk.percent, 2),
        "Memory Percent": round(vm.percent, 2),
        "Disk Free": round(disk.free / (1024**3), 2),
        "Disk Total": round(disk.total / (1024**3), 2),
        "Disk Used": round(disk.used / (1024**3), 2),
        "Memory Total": round(vm.total / (1024**3), 2),
        "Memory Active": round(getattr(vm, "active", 0) / (1024**3), 2),
        "Memory Available": round(vm.available / (1024**3), 2),
        "Memory Cached": round(getattr(vm, "cached", 0) / (1024**3), 2),
        "Memory Free": round(vm.free / (1024**3), 2),
        "Memory Used": round(vm.used / (1024**3), 2)
    }

def get_network_info():
    net_io = psutil.net_io_counters()
    return {
        "Hostname": socket.gethostname(),
        "Ip Address": socket.gethostbyname(socket.gethostname()),
        "Network Bytes Received": round(net_io.bytes_recv / 1024, 2),
        "Network Bytes Sent": round(net_io.bytes_sent / 1024, 2),
        "Network Packets Recv": net_io.packets_recv,
        "Network Packets Sent": net_io.packets_sent
    }

def get_uptime():
    uptime_seconds = int(time.time() - psutil.boot_time())
    days, remainder = divmod(uptime_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{days}d {hours}h {minutes}m {seconds}s"

def get_minimal_metrics(runtime_metrics, temperature_info):
    # Return only critical usage stats and temps
    minimal = {}

    # Critical runtime usage stats keys to keep:
    critical_keys = [
        "Cpu Percent",
        "Memory Percent",
        "Disk Percent",
    ]
    for key in critical_keys:
        if key in runtime_metrics:
            minimal[key] = runtime_metrics[key]

    # Add all temperature sensors (with keys prefixed for clarity)
    for sensor_name, temp in temperature_info.items():
        minimal[f"Temp {sensor_name} (°C)"] = temp

    return minimal

def get_all_metrics():
    system_info = get_system_info()
    runtime_metrics = get_runtime_metrics()
    network_info = get_network_info()
    temperature_info = get_temperature_info()
    uptime = get_uptime()

    minimal_metrics = get_minimal_metrics(runtime_metrics, temperature_info)

    return {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "system_info": system_info,
        "runtime_metrics": runtime_metrics,
        "network_info": network_info,
        "temperature": temperature_info,
        "uptime": uptime,
        "minimal_metrics": minimal_metrics
    }

if __name__ == "__main__":
    import json
    print(json.dumps(get_all_metrics(), indent=2))
