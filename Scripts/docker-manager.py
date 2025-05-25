# Python script to manage my Docker containers
import os
import sys
import subprocess

SWARM_DIR="/home/jlw/Swarms"
STACKS = {
    "DEPi-core": f"{SWARM_DIR}/core.yml",
    "DEPi-auxiliary": f"{SWARM_DIR}/aux.yml",
    "DEPi-Nextcloud": f"{SWARM_DIR}/nextcloud.yml",
    "DEPi-monitor": "/home/jlw/DEPi/Cluster-Monitor/docker-compose.yml"
}

def run_command(command):
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exception: {e}")
        sys.exit(e.returncode)

def start_stack(stack_name, path):
    print(f"Starting {stack_name} from {path}...")
    run_command(["docker", "stack", "deploy", "-c", path, stack_name])
    
def main():
    for name, path in STACKS.items():
        start_stack(name, path)
    print("All stacks started :)")

if __name__ == "__main__":
    main()