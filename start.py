import os.path
from Bot import Bot

#create/load settings file
fileName = "settings.cfg"

if(os.path.isfile(fileName)): #file exists
	file = open(fileName, "r")
	lines = list(file)
	username = lines[0].rstrip('\n')
	password = lines[1].rstrip('\n')
	ip = lines[2].rstrip('\n')
	port = lines[3].rstrip('\n')
	file.close()
else: #file does not exist
	while True:
		username = input("Enter username: ")
		password = input("Enter password: ")
		ip = input("IP: ")
		port = input("Port: ")
		if(username != "" and password != "" and ip != "" and port != ""):
			break
	saveSettings = input("Save settings in plain text? (y/n) ")
	if saveSettings == "y" or saveSettings == "Y" or saveSettings == "yes" or saveSettings == "Yes":
		file = open(fileName, "w")
		file.write(username + "\n")
		file.write(password + "\n")
		file.write(ip + "\n")
		file.write(port)
		file.close()

#Send parameters to real bot
Bot.Connect(username, password)