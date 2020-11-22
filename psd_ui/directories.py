import winreg
from pathlib import Path

def EmptyFolder(path):
	for child in path.iterdir():
		if child.is_file():
			child.unlink()
		else:
			EmptyFolder(child)
			child.rmdir()

def GetOutputPath(filename):
	name = Path(filename).stem
	path = Path("output/" + name + "/images")
	path.mkdir(parents=True, exist_ok=True)
	EmptyFolder(path)
	return path

def GetContentPath():
	access_registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
	access_key = winreg.OpenKey(access_registry, r"Software\Roblox\RobloxStudio")

	if access_key:
		path = winreg.QueryValueEx(access_key, "ContentFolder")[0]
		access_key.Close()
		return Path(path)

def GetDebugPath(name):
	contentPath = GetContentPath()
	path = Path(contentPath.as_posix() + "/psd_ui/" + name)
	path.mkdir(parents=True, exist_ok=True)
	EmptyFolder(path)
	return path

def GetStoredCookie():
	cookieFile = Path("cookie.txt")
	if cookieFile.is_file():
		return open(cookieFile.as_posix(), "r").read()
	return False