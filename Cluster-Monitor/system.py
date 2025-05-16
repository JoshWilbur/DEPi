import platform
import psutil
import socket

def get_system_info():
    # Dict for system information 
    sys_info = {
        "OS": platform.system(),
        "OS Release": platform.release(),
        "Architecture": platform.architecture()[0],
        "Machine": platform.machine(),
        "Processor": platform.processor(),
        "CPU Cores (Logical)": psutil.cpu_count(logical=True),
        "CPU Cores (Physical)": psutil.cpu_count(logical=False),
        "RAM": f"{round(psutil.virtual_memory().total / (1024**3), 2)} GB",
        "Python Version": platform.python_version(),
        "Platform": platform.platform(),
        "Node": platform.node(),
        "Boot Time": psutil.boot_time(),
    }
    return sys_info


def get_network_info():
    # Dict for network information
    nw_info = {
        "Hostname": socket.gethostname(),
        "IP Address": socket.gethostbyname(socket.gethostname())
    }
    return nw_info

if __name__ == "__main__":
    system_info = get_system_info()
    nw_info = get_network_info()
    for key, value in system_info.items():
        print(f"{key}: {value}")
    for key, value in nw_info.items():
        print(f"{key}: {value}")
