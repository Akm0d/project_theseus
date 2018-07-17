# Project Theseus
This project is forked from the private repo of the OpenWest Defusal Station project. It is named "Project Theseus" after the paradox of the Ship of Theseus; a thought experiment that raises the question of whether an object that has had all of its components replaced remains fundamentally the same object.

# Contribution Guidelines
1. Create a branch for your code and merge it to master once the changes are stable
2. Keep the file structure as organized as possible
3. Never commit binaries, hidden files created by your IDE, or Windows-style line endings.
4. Keep detailed comments of what each function is meant to do
5. Follow the PEP-8 standard when writing python https://www.python.org/dev/peps/pep-0008/
6. Use comments starting with TODO to mark a feature that needs to be implemented and FIXME to mark features that need to be improved
7. If you are stuck, then it is absolutely OK to ask for help

# Getting Started
```bash
$ sudo apt-get update
$ sudo apt-get install python3 git python3-pip
$ git clone https://github.com/jtylers/project_theseus.git
$ cd project_theseus
$ git submodule update --init
$ pip3 install -r requirements.txt
$ ./serve.py
$ firefox 127.0.0.1:5000
```
I highly suggest using PyCharm if you are working with Flask and Python
```bash
$ sudo apt-get update
$ sudo apt-get install snapd
$ snap install pycharm-community
```
Add the project root to your python path for things to run correctly
```bash
$ echo "export PYTHONPATH=$PYTHONPATH:$HOME/project_theseus" >> ~/.profile
$ source ~/.profile
```

## Raspberry pi - ARCH Linux Setup
```bash
$ ## login with user: root password: root
$ # Delete default user
$ userdel alarm
$ # Create a new adminuser
$ useradd admin
$ # Set password for admin
$ passwd admin
$ # Make a home folder for admin
$ mkdir -p /home/admin
$ # Change ownership of the admin's home folder
$ chown -R admin:admin /home/admin
$ pacman -S sudo
$ # Grant admin sudo privileges
$ visudo
$ ## Press SHIFT + G then SHIFT + A
$ ## type "admin ALL=(ALL) ALL" without the quotes
$ ## save and quit by pressing ESCAPE, typing ":x" and pressing ENTER
$ # Remove root's password entry so that you can only log in as "admin" and use sudo and to do root stuff
$ vim /etc/shadow
$ ## replace root's password hash with !
$ # Install dependencies
$ pacman -S fakeroot gcc git i2c-tools make packer python python-dateutil python-flask python-flask-restful python-pip tmux vim 
$ packer -S raspi-config
$ # Enable I2C 
$ echo "dtparam=i2c_arm=on"| sudo tee -a /boot/config.txt
$ sudo reboot
$ ## Log in as admin
$ ## Allow admin to access i2c
$ sudo chown admin:admin /dev/i2c*
$ ## Proceed with the instructions from the "Getting Started" section
```

## Setting up a Pi to have the same ipv6 address on any network
```bash
$ cd project_theseus
$ pacman -S radvd
$ sudo cp radvd.conf /etc/radvd.conf
$ sudo cp ipv6 /usr/local/bin/ipv6
$ sudo /usr/local/bin/ipv6
$ sudo systemctl restart radvd
```

## Where are variables stored?
Stored in the database
```
ID
Name
Laser   -- Deprecated
Code
Color
Time    -- Stored as a datetime object but written at end of game
Success
```
