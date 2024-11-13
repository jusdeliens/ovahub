# ovahub
MQTT Broker tools for administrating [Ova bots](https://jusdeliens.com/ova) and Jusdeliens [IDEAL games](https://jusdeliens.com/ideal-arena/)

## 🎯 Context

`OvaHub` is a CLI tool to allow any user to administrate its own mqtt broker on a **L**ocal **A**rea **N**etwork to play with  [Ova bots](https://jusdeliens.com/ova) and Jusdeliens [IDEAL arena games](https://jusdeliens.com/ideal-arena/).

## 🌐 Network architecture

In all Jusdeliens' games, each player controls a robot in a virtual/augmented arena, through its computer, thanks to an AI program implemented to automatically assess the robot environment and perform actions to lead it to victory 🏆 !

But as any game, there are rules to comply with ! And so, every requests shall be received and checked by a "referee program" (who does the same as a soccer referee in a football stadium ⚽︎), before every change can happen in the game.

To be able to link all these following endpoints ...
- each robot of every player
- the AI program implemented by each player to control its robot, and which can be ran on the player's computer IDE (or on a dedicated server)
- the arena server with its referee program
- the arena viewers on each player computer browser, in order to render and see the virtual/augmented arena effects (map, ressources, fires & other special effects)

... a robust network shall be implemented, with high performance & security constraints, both
- physically : by using a 2.4Ghz wifi access point (embedding a DHCP server to automatically distribute IP to every endpoints), with credentials saved in each robot and computers to secure the physical access to the network
- logically : by using a MQTT broker, to work as a logic mediator between all the endpoints, by allowing to secure who can read/write to who in what conditions thanks to editable ACL (Access Control List).
 
![Network architecture diagram](/doc/arch.svg "Network architecture diagram") 

*This diagram is generated from `doc/arch.wsd` with **plantUML** extension in VSCode*


## 🛠️ Setup

To deploy a broker, you need to be on an admin session with the following software installed
- [Docker Engine](https://www.docker.com/products/docker-desktop/) 
- as well as [git](https://www.git-scm.com/downloads)
- and [VSCode](https://code.visualstudio.com/download) IDE

First, clone this project from our github
```
git clone https://github.com/jusdeliens/ovahub.git
```

Then start Docker Engine as administrator. According to your OS, the Docker installation process may be different :

### 🪟 Windows

Install [Docker Desktop]() on a session with admin rights. Also, make sure you have the [WSL2 kernel update](https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi) installed on your windows. If not, you will have to install it at the end of Docker Desktop installation. 
Click here if you want to [know more about WSL](https://learn.microsoft.com/fr-fr/windows/wsl/install).

### 🐧 Unix

[Follow theses steps](https://docs.docker.com/desktop/install/linux-install/) to install Docker Desktop whether you are on Ubuntu, Debian, Fedora or Arch.

## 🚀 Deploy

Once Docker Desktop started on your admin session, follow theses steps

### 🔑 Create users and password 
When using Jusdeliens product, you should have at least 3 users :
- `demo` : for non admin users with a simple password
- `admin` : only for 1 admin user with a strong password
- `ova` : username used by ova bots

Usernames and password must be stored encrypted in the `passwd.ini` file. To do it, simply use `CTRL+SHIFT+B` shortcut in VSCode and select the task `Register users and passwords`.

Otherwise, you can use the following command in a elevated shell (`gitbash` for instance) in the project dir :

```
python ovahub.py regusr
```

This will ask you in the console the username and password for each user to add. Once the task is complete, the passwd file will contain per line the username followed by `:` then the encrypted password

⚠️ Carefull, when running this command, all previous users stored in `passwd.ini` are deleted. 

### 🐳 Start the broker 

Once the user created, let's run the broker on your LAN ! use `CTRL+SHIFT+B` shortcut in VSCode and select the task `Start broker in a local container`, or use the following command :

```
python ovahub.py start
```

This should start the broker and display your network informations to give to user so that they could connect to your broker :

```
🟢 The broker may now be online on LAN at x.x.x.x, with following available ports for clients 👇
📬 mqtt: 1883
📬 ws: 9001
If not, check your network connection and your firewall
To join/admin an arena, open this url your web browser
👉 http://play.jusdeliens.com/login/?viewer=tactx&url=192.168.x.x&port=8080&usr=admin&pwd=&pseudo=admin&show=address_port_username_password_viewer
```

> [!NOTE]  
> `x.x.x.x` shall be replaced by (one of) your local ip address.
> If you have other network interfaces, feel free to use another one
> using `ipconfig` or `ifconfig` command in your shell.

Then, this kind of successfull logs

```
1718315757: mosquitto version 2.0.18 starting
1718315757: Config loaded from /mosquitto/config/mosquitto.conf.
1718315757: Opening ipv4 listen socket on port 1883.
1718315757: Opening ipv6 listen socket on port 1883.
1718315757: Opening websockets listen socket on port 9001.
1718315757: mosquitto version 2.0.18 running
```

If not, check 
- your firewall so that it allows the mqtt and ws port to be opened
- your network connection  

Now you can fully enjoy playing with Ova bots and IDEAL games without any constraints. Feel free to administrate your broker as you want by changing `acls.ini` `mosquitto.conf` and `passwd.ini`. Go on the [eclipse manual page](https://mosquitto.org/man/mosquitto-conf-5.html) to know more about how to do it.

If you need more help, feel free to [contact us](https://jusdeliens.com/contact) to join our robotic masterclasses 🤖

## 📁 Project structure

- **.vscode** : IDE settings tasks to be loaded in VScode using `CTRL+SHIFT+B` shortcut
- **mosquitto** : Broker folder with all configurations files, logs and store data
    - **config** : Contains the `acls.ini` `passwd.ini` `mosquitto.conf` file to configure the broker settings
    - **data** : Stores the data exchanged in a database in `mosquitto.db` once the broker is started
    - **log** : Where `mosquitto.log` will be filled with debug informations according to the verbosity set in `mosquitto.conf` file
- **doc**: documentation diagrams generated using plantUML

## 🧑‍💻 Author
Designed with 💖 by [Jusdeliens Inc.](https://jusdeliens.com)

## ⚖️ Licence
Under [CC BY-NC 4.0 licence](https://creativecommons.org/licenses/by-nc/4.0/deed.en) 
