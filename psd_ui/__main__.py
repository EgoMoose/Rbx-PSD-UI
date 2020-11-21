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
	cookie = input("Please provide the account cookie you want to upload these images with:\n")
	if VerifyUsername(cookie):
		process(args.psd, outputPath, None, cookie)
else:
	contentPath = directories.GetDebugPath(outputPath.stem)
	process(args.psd, outputPath, contentPath, None)