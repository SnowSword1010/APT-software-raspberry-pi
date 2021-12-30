# **APT-software-raspberry-pi**

Raspberry Pi Autostart software created for APT Electronics Pvt Ltd.

## **Pre-config raspberry pi**

<!-- OL -->
1. Uncomment and set ```hdmi_group=2``` and ```hdmi_force_hotplug=1``` in config.txt of memory card where raspbian is installed
2. Set ```hdmi_mode=39``` in config.txt
3. Enable ssh
4. Install vim (gvim installation optional, but recommeneded)
  ```bash
   sudo apt install vim
   ```
   ```bash
   sudo apt-get install vim-gtk

   ```   
5. Install image-magick
  ```bash
   sudo apt-get install imagemagick
   ```
   
## **Setup**
1. Disable the firewall permanently
<!-- UL -->
  - Temporarily stop firewall
  <!-- Code Block -->
  ```bash
    sudo systemctl stop firewalld
  ```
  - Disable the firewall service at boot time
  <!-- Code Block -->
  ```bash
    sudo systemctl disable firewalld
    sudo systemctl mask --now firewalld
  ```
  - Check status of your firewall (recommended to reboot the system)
  <!-- Code Block -->
  ```bash
    sudo firewall-cmd --state
  ```

2. Disable iptables rules
<!-- Code Block -->
  ```bash
    iptables -F
  ```
3. Navigate to desktop and paste
```bash
   git clone https://github.com/SnowSword1010/APT-software-raspberry-pi.git
```
4. cd into the folder
```bash
   cd APT-software-raspberry-pi
```
5. Install requirements.txt
```bash
   pip3 install -r requirements.txt
```
6. Test using
```bash
   python3 receiveImg.py
```

## **Autostart Guidelines**
1. Navigate to .config directory (hidden)
```bash
   sudo cd /home/pi/.config
```
2. Create a directory called autostart if it is not present
```bash
   mkdir autostart
```
3. Create a file called autorun.desktop
```bash
   touch autorun.desktop
```
4. Paste the following
```bash
   [Desktop Entry]
   Exec= python3 /home/pi/Desktop/APT-software-raspberry-pi/receiveImg.py
```
5. Save and exit
