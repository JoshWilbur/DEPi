# DEPi

Pi cluster for home automation and self-hosting! I'll get around to making a more detailed description in the future...

# Software Stack

I host a variety of services to gain experience with sysadmin work and save cost. Here is a table of the software I run:

| Service Name                | Description                       | Additional Notes                                                                                       | Replaces     |
| --------------------------- | --------------------------------- | ------------------------------------------------------------------------------------------------------ | ------------ |
| Portainer                   | GUI manager for Docker containers | Excellent piece of software, worked out of the box.                                                    | N/A          |
| Technitium                  | DNS server and blocker            | Advanced DNS server that supports forwarding<br />over TLS. Great for security purposes.               | N/A          |
| Code Server                 | Web-based VS code                 | Useful if I need to code on an external computer.                                                      | N/A          |
| Wireguard                   | VPN for cluster                   | Painful to get running, took a lot of attempts. Totally<br />worth the setup pain, had no issues since | N/A          |
| Cluster Monitor             | Displays cluster stats            | Can be found in Cluster-Monitor                                                                        | N/A          |
| Nextcloud                   | Self-hosted cloud                 | Feature-rich cloud that supports mobile access.                                                        | Google Drive |
| Miniflux                    | RSS feed                          | Works as intended, nothing special                                                                     | RSS.app      |
| EmulatorJS                  | ROM Emulator                      | Works for all retro consoles                                                                           | NES/SNES     |
| Docker Bench<br />Security* | Security audit for Docker         | Only ran occasionally after updates                                                                    | N/A          |
| Focalboard*                 | Ticket-based planner              | Useful for small projects, unused otherwise                                                            | Jira         |

NOTE: Any software with a star (*) appended to it means it is only used occasionally or as needed

# Hardware

**Current Setup:**

* Raspberry Pi 5, 8GB
* Raspberry Pi 5, 4GB
* Raspberry Pi 2B
* Real HD PoE Switch
* Patch cables and PoE HATs
