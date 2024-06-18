# -*- coding: utf-8 -*-
#                           ██╗██████╗ ██╗           
#                           ██║╚════██╗██║           
#                           ██║ █████╔╝██║           
#                      ██   ██║██╔═══╝ ██║           
#                      ╚█████╔╝███████╗███████╗      
#                       ╚════╝ ╚══════╝╚══════╝      
#                       https://jusdeliens.com
#
# Designed with 💖 by Jusdeliens
# Under CC BY-NC 4.0 licence
# https://creativecommons.org/licenses/by-nc/4.0/deed.en
#  
# Be sure to use a unix shell (gitbash on Windows)

import os
import subprocess
import time
import sys
from getpass import getpass

def error(msg, endl="\n"):
	msg = "🚨 "+msg
	print(msg, end=endl)
def warning(msg, endl="\n"):
	msg = "⚠️  "+msg
	print(msg, end=endl)
def info(msg, endl="\n"):
	print(msg, end=endl)
def ospathjoin(path:str, *paths):
	return os.path.join(path, *paths)
def getWorkingDir():
	return os.getcwd()


config = {
	"config-dir": [ospathjoin(getWorkingDir(), "mosquitto", "config"), 
		"The mosquitto dir where to find conf.ini"],
	"data-dir": [ospathjoin(getWorkingDir(), "mosquitto", "data"), 
		"The mosquitto dir where to find database backup"],
	"log-dir": [ospathjoin(getWorkingDir(), "mosquitto", "log"), 
		"The mosquitto dir where to find logs"],
	"name": ["ovahub",
		"The name of the docker container running the broker"],
	"mqtt-port": ["1883", 
	    "The default port for mqtt clients"], 
	"ws-port": ["8080",
		"The websocket port for web browser clients"] ,
	"img": ["eclipse-mosquitto:latest", 
	 	"The broker image to download from docker repo"],
	"os": ["win", 
		"The host machine os. 'win' = windows, 'unix' = linux, mac ... "],
	"arena": ["", 
		"The name of the default arena to join "],
	"viewer": ["tactx", 
		"The of the html folder on viewer website. Can be 'robots','tactx','xihara'"]
}

def run(cmd, sudo=False, targetOS=config["os"][0], debug=True):
	"""Run a cmd in the actual bash"""
	if ( sudo and targetOS=="unix"):
		cmd = "sudo -S -p '' "+ cmd
	if debug:
		info("> "+cmd)
	subprocess.call(cmd, shell=True)

def help():
	"""Display the manual with all options"""
	print()
	print("Usage: python3 ovahub.py COMMAND [OPTION]")
	print()
	print("Administrate your own LAN mqtt broker in a unix shell to play with Jusdeliens Ova bots and IDEAL games")
	print()
	print("Sample:")
	print("\tTo start mqtt broker container listening 1883 and 8080 port on a windows host machine")
	print("\t> python ovahub.py start --mqtt-port 1883 --ws-port 8080 --os win")
	print()
	print("Options:")
	for key,value in config.items():
		print(f"\t--{key}")
		print(f"\t\t{value[1]}")
		print(f"\t\tdefault: '{value[0]}'")
		print()
	print()
	print("Commands:")
	for key,value in cmd.items():
		print(f"\t{key}\t{value[1]}")
	exit()

def stop():
	"""Stop and remove the broker container"""
	containersToStop = [config["name"][0]]
	for containerName in containersToStop:
		try:
			info("⏳ Clearing old container and image ... ")
			cmds = ["docker stop "+containerName, "docker rm "+containerName]
			for cmd in cmds:
				run(cmd, sudo=True)
		except Exception as e:
			error("Fail stopping docker"+": "+str(e))
			raise SystemExit

def clear():
	"""Clearing old logs"""
	dirsToRemove = []
	filesToRemove = [ospathjoin(config["log-dir"][0],"*.log")]
	for dirToRemove in dirsToRemove:
		info("⏳ Removing build dir "+dirToRemove+"... ", endl="\n")
		try:
			run("rm -rf "+dirToRemove, sudo=True)
			info("✅")
		except Exception as e:
			info("❌")
			warning("Fail to remove build dir "+dirToRemove+""+": "+str(e))
	for fileToRemove in filesToRemove:
		info("⏳ Removing build file "+fileToRemove+"... ", endl="\n")
		try:
			run("rm "+fileToRemove, sudo=True)
			info("✅")
		except Exception as e:
			info("❌")
			warning("Fail to remove file "+fileToRemove+""+": "+str(e))
		
def start():
	"""Called when 'start' command is specified
	TODO: add prompt to set verbosity in conf
	"""
	try:
		stop()
		clear()
	except:
		...
	info("⏳ Starting container ... ")
	run(f'docker run -dit --restart unless-stopped -v {config["config-dir"][0]}/:/mosquitto/config -v {config["data-dir"][0]}/:/mosquitto/data -v {config["log-dir"][0]}/:/mosquitto/log -p {config["mqtt-port"][0]}:1883 -p {config["ws-port"][0]}:9001 --name {config["name"][0]} {config["img"][0]}', sudo=True)

	try:
		import socket
		hostname = socket.gethostname()
		ip_address = socket.gethostbyname(hostname)
		info("")
		info(f"🟢 The broker may now be online on LAN at {ip_address}, with following available ports for clients 👇")
		info(f"📬 mqtt: {config['mqtt-port'][0]}")
		info(f"📬 ws: {config['ws-port'][0]}")
		info("If not, check your network connection and your firewall")
		info("")
		info(f"To join/admin an arena, open this url your web browser")
		info(f"👉 http://play.jusdeliens.com/login/?arena={config['arena'][0]}&viewer={config['viewer'][0]}&url={ip_address}&port={config['ws-port'][0]}&usr=admin&pwd=&pseudo=admin&show=address_port_username_password_viewer")
		info("")
		info(f"To join arena as user, open this url your web browser")
		info(f"👉 http://play.jusdeliens.com/login/?arena={config['arena'][0]}&viewer={config['viewer'][0]}&url={ip_address}&port={config['ws-port'][0]}&usr=demo&pwd=&pseudo=&show=address_port_username_password_pseudo")
		info("")
		time.sleep(1)
	except:
		...

	logfile = ospathjoin(config["log-dir"][0],"mosquitto.log")
	info(f"⏳ Debuging log from {logfile} ...")
	info("💡 Press CTRL+C to interrupt debug once started")
	time.sleep(10)
	run(f"tail -F {logfile}")

def regusr():
	"""
	TODO: Add explicit message for each username and password prompt
	TODO: Add link at the end to open the passwd.ini file
	"""
	pwdfilepath = ospathjoin(config["config-dir"][0],"passwd.ini")
	with open(pwdfilepath, 'w', encoding='utf-8') as f:
		defaultUsernames = ["admin", "demo", "ova"]
		users = {}
		while True:
			usrname = None
			for defaultUsr in defaultUsernames:
				if defaultUsr not in users:
					usrname = defaultUsr
					print()
					print(f"Set the password for required user\n👤 {usrname}")
					break
			if usrname == None:
				print()
				print("Add new users and password.")
				print("Press Enter with empty username to stop.")
				usrname = input("👤 username: ")
				if len(usrname) == 0:
					break
			while True:
				print("🔑 password: ")
				usrpwd = getpass(">")
				if len(usrpwd) < 4:
					print("⚠️ Enter a stronger password (>4 characters)")
				else:
					break
			users[usrname] = usrpwd
		for usrname, usrpwd in users.items():
			f.write(f"{usrname}:{usrpwd}\n")			
        # your logic goes right here
	run(f'docker run -it --rm -v {config["config-dir"][0]}/:/mosquitto/config --name {config["name"][0]}-regusr {config["img"][0]} mosquitto_passwd -U /mosquitto/config/passwd.ini', sudo=True)


cmd = {
	"start": [start, "Start the broker container"],
	"stop": [stop, "Stop the broker container"],
	"regusr": [regusr, "Clear all previous users added, then add users and passwords in passwd ini file"],
	"help": [help, "Display the man page"]
}

os.system("chcp.com 65001")
os.system("export PYTHONIOENCODING=utf-8")
os.system("export LANG=en_US.UTF-8")

nArg = len(sys.argv)
iArg = 1
cmdArg = "help"
while iArg<nArg:
	argName = sys.argv[iArg]
	argValue = None
	if iArg == 1:
		if argName in cmd:
			cmdArg = argName
	elif ( iArg+1 < nArg ):
		argValue = sys.argv[iArg+1]
		argKey = argName.replace("--","")
		if argKey in config:
			info(f"Changed config '{argName}' from '{config[argKey][0]}' to '{argValue}'")
			config[argKey][0] = argValue
			iArg += 1
	iArg+=1
cmd[cmdArg][0]()

