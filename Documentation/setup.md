# DEPi Setup Guide
The software stack and configuration for DEPi is here. 

**Before First Boot**
Prior to setup, an OS must be installed on the main and worker nodes. I'm using Raspberry Pi OS Lite for all of the Pi boards, note that the Pi 2B 
only supports 32 bit. Be sure to set a hostname and SSH key for these devices to avoid future headaches. Construct all the hardware provided in the BOM
according to the instructions in the box.

**Initial Setup**
* Generate an SSH key for the node, be sure to only allow private key login when flashing the OS onto an SD card.
* Connect all nodes to the PoE switch
* Load the SSH key using `ssh-add keyname`
* SSH into each node before continuing. **NOTE:** If the Pi 5 gives an error LED signal on startup, try re-flashing the bootloader.
* On each node, run `sudo apt update && sudo apt upgrade -y` to update the system and packages.
* Edit /etc/hosts with root permissions and associate IP addresses with node names.
* Generate key pair on main node with `ssh-keygen -t rsa` then use `ssh-copy-id` for all nodes. Test SSH on all nodes before continuing.
* Using apt, install the following packages on the main node: htop, vim, ansible, clusterssh, tmux
* Set up ansible inventory file `vim ~/path/ansible_hosts`. Syntax is similar to the Linux hosts file. 
* Run `ansible -i ~/ansible_hosts all -m ping` to verify the prior step. In typical Linux fashion, ping returns pong.
* Initial setup is complete, from here the cluster configuration is use-case specific.

**Pi-Hole**
* On a worker node, run `curl -sSL https://install.pi-hole.net | bash`

