import re
import requests
import subprocess

TARMAC_TOML = '''
name = "{0}"

[[inputs]]
glob = "{1}/*.png"
codegen = true
codegen-path = "{1}/assetids.lua"
codegen-base-path = "{1}"
'''

HEADERS = {
	"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:66.0) Gecko/20100101 Firefox/66.0",
	"Accept": "application/json, text/plain, */*",
	"Accept-Language": "en-US,en;q=0.5",
	"Content-Type": "application/json;charset=utf-8",
	"Origin": "https://www.roblox.com",
	"X-CSRF-TOKEN": "",
	"DNT": "1",
}

def VerifyUsername(cookie):
	try:
		response = requests.get("https://www.roblox.com/game/GetCurrentUser.ashx", cookies={".ROBLOSECURITY": cookie}, headers=HEADERS)
		response = requests.get("https://api.roblox.com/users/" + response.text)
		username = response.json().get("Username")
		valid = input("The username assosiated with this cookie is " + username + ". Is this correct? (y/n) : ")
		return valid == "y"
	except:
		print("Something was wrong with the cookie provided. Ensure it's a valid account cookie.")
		return False

def TarmacSync(outputPath, cookie):
	parentPath = outputPath.parent
	subPath = "/".join(outputPath.parts[-1:])

	f = open(parentPath.as_posix() + "/tarmac.toml", "w")
	f.write(TARMAC_TOML.format(parentPath.stem, subPath))
	f.close()

	subprocess.run([
		"tarmac", "sync", 
		"--target", "roblox",
		"--auth", cookie
	], cwd = parentPath.as_posix())

	f = open(outputPath.as_posix() + "/assetids.lua", "r")
	matches = re.findall(r'\S+_(\d+) = "(rbxassetid://\d+)"', f.read())

	arr = []
	for match in matches:
		index = int(match[0]) - 1
		arr.insert(index, match[1])

	return arr