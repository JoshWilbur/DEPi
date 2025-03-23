# DEPi Software

The software stack and configuration for DEPi is here. This is mostly for my own purposes in case I need to reinstall. Making it public in case it can help anyone else.

**Containers Running Currently**
* Portainer: Management of containers
* Technitium: DNS server
* Netdata: Cluster monitoring
* Code Server: Remote code environment

# DEPi Setup

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
* Edit /etc/hosts with root permissions and associate IP addresses with node names. I used `hostname -I` on all nodes.
* Generate key pair on main node with `ssh-keygen -t rsa` then use `ssh-copy-id` for all nodes. Ensure each node has the public key within ~/.ssh/authorized_keys
* Using apt, install the following packages on the main node: htop, vim, ansible, clusterssh, tmux
* Set up ansible inventory file `vim ~/path/ansible_hosts`. Syntax is similar to the Linux hosts file.
* Run `ansible -i ~/ansible_hosts all -m ping` to verify the prior step. In typical Linux fashion, ping returns pong.

After this, the cluster is "working" in the most basic sense. However, it lacks features which make clusters fun and useful. I'm choosing to use Docker for my containers due to prior experience. Details on that and other services I installed are below.

**Docker**

* Install using `sudo apt install -y docker.io docker-compose`
* Optional: add user to Docker group `sudo usermod -aG docker $USER` (reboot after this)
* Test out Docker with a classic program `docker run hello-world`
* Install portainer if you want a GUI to manage containers, some people may benefit more from that.

**Docker Compose**
See docker-compose.yml as it contains all of my containers and setup. I'm using Docker swarm to deploy across my nodes.
* Deploy swarm with `docker stack deploy -c docker-compose.yml DEPi-Stack`
* Check with `docker stack services DEPi-Stack`
* Remove swarm with `docker stack rm DEPi-Stack`

**Technitium DNS Filtering**

* Settings are in docker-compose.yml
* Upload [Blacklist](https://github.com/StevenBlack/hosts) to DNS server settings
* Set DEPi-Main IP address as router's primary DNS server (1.1.1.1 as a backup when DEPi is down)
* DNS filtering should be active now

**Grafana**
Grafana has a great tutorial on their website. Rather than rewrite it here, I'll just paste the url. Note: Prometheus also needs to be installed
[grafana tutorial](https://grafana.com/docs/grafana/latest/setup-grafana/installation/docker/)
[prometheus tutorial](https://prometheus.io/docs/prometheus/latest/getting_started/)
Here is my list of metrics:

**WireGuard**
I tried out two different ways to run WG. The Docker solution seemed much simpler, but leaving the manual way up for future reference.\\
UPDATE: I'm switching to a router-based VPN for security reasons.

* To install, run `sudo apt install wireguard wireguard-tools -y`
* Generate public and private keys `wg genkey | tee wg_privatekey | wg pubkey > wg_publickey`
* Follow this guide for the rest [Guide](https://wiresock.net/documentation/wireguard/config.html)
* Be sure to put the wireguard config file in /etc/wireguard/wg0.cong
* Bring server up with `sudo wg-quick up wg0`
* Bring server down with `sudo wg-quick down wg0`
* Enable at boot with `sudo systemctl enable wg-quick@wg0`