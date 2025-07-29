# Migrating Networks

The software stack and configuration for DEPi is here. This is mostly for my own purposes in case I need to reinstall. Making it public in case it can help anyone else.

**Changing Subnet**
* Mount Pi SD card to a PC
* Do one of the following
* Remove all files under /etc/NetworkManager/system-connections
* Edit /etc/systemd/network/10-eth0.network
* Recreate docker swarm