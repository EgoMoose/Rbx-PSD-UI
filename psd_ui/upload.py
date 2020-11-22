import re
import requests

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

def UploadImage(imagePath):
	return -1