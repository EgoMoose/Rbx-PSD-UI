import argparse
import directories
from upload import VerifyUsername
from process import main as process

parser = argparse.ArgumentParser()
parser.add_argument("psd", type = str, help = "The relative path to the psd file.")
parser.add_argument("-u", "--upload", action="store_true", help = "Flag for if the psd should be uploaded to Roblox.")
args = parser.parse_args()

outputPath = directories.GetOutputPath(args.psd)

if args.upload:
	cookie = directories.GetStoredCookie()
	if not cookie:
		cookie = input("Please provide the account cookie you want to upload these images with:\n")
		if VerifyUsername(cookie):
			process(args.psd, outputPath, None, cookie)
	else:
		# you can use a stored cookie if you don't want to constantly copy/paste
		process(args.psd, outputPath, None, cookie)
	print("PSD successfully processed and upload to Roblox complete.")
else:
	contentPath = directories.GetDebugPath(outputPath.parent.stem)
	process(args.psd, outputPath, contentPath, None)
	print("PSD successfully processed.")