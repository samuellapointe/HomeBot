import os.path

#create/load settings file
fileName = "settings.cfg"

if(os.path.isfile(fileName)): #file exists
	file = open(fileName, "r")
	lines = list(file)
	username = lines[0].rstrip('\n')
	password = lines[1]
	file.close()
else: #file does not exist
	while True:
		username = input("Enter username: ")
		password = input("Enter password: ")
		if(username != "" and password != ""):
			break
	saveSettings = input("Save settings in plain text? (y/n) ")
	if saveSettings == "y" or saveSettings == "Y" or saveSettings == "yes" or saveSettings == "Yes":
		file = open(fileName, "w")
		file.write(username + "\n")
		file.write(password)
		file.close()

print(username + ", " + password)