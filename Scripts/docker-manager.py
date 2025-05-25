# Python script to manage my Docker containers
import os
import sys
import subprocess

SWARM_DIR="/home/jlw/Swarms"
STACKS = {
    "DEPi-core": f"{SWARM_DIR}/core.yml",
    "DEPi-auxiliary": f"{SWARM_DIR}/aux.yml",
    "DEPi-nextcloud": f"{SWARM_DIR}/nextcloud.yml",
    "DEPi-monitor": "/home/jlw/DEPi/Cluster-Monitor/docker-compose.yml"
}

def start_stack(path, stack_name):
    print(f"Starting {stack_name} from {path}...")
    run_command(["docker", "stack", "deploy", "-c", path, stack_name])
    
def main():
    for name, path in STACKS.items():
        start_stack(name, path)
    print("All stacks started :)")

if __name__ == "__main__":
    main()