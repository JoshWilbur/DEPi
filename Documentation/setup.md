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
* Ensure you can connect to every node of the cluster before continuing.