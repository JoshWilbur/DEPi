# DEPi Setup Guide
The software stack and configuration for DEPi is here. This is mostly for my own purposes in case I need to reinstall. Making it public in case it can help anyone else.

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

After this, the cluster is "working" in the most basic sense. However, it lacks features which make clusters fun and useful. I'm choosing to use Docker for my containers due to prior experience. Details on that and other services I installed are below.

**Docker**
* Install using `sudo apt install -y docker.io docker-compose`
* Optional: add user to Docker group `sudo usermod -aG docker $USER` (reboot after this)
* Test out Docker with a classic program `docker run hello-world`
* Install portainer if you want a GUI to manage containers, some people may benefit more from that.

**Technitium DNS Filtering**
* Upgrade then install dependencies `sudo apt install -y libicu-dev libssl-dev libkrb5-3`
* Download Technitium with Docker `docker pull technitium/dns-server:latest` then `docker volume create portainer_data`
* Run using `docker run -d --name=technitium --restart=always -p 53:53/tcp -p 53:53/udp -p 5380:5380/tcp -v ~/Logs/technitium:/etc/dns technitium/dns-server`
* More setup to come later

**Grafana**
Grafana has a great tutorial on their website. Rather than rewrite it here, I'll just paste the url. Note: Prometheus also needs to be installed \
[grafana tutorial](https://grafana.com/docs/grafana/latest/setup-grafana/installation/docker/)
[prometheus tutorial](https://prometheus.io/docs/prometheus/latest/getting_started/)
Here is my list of metrics:


**OpenVPN**