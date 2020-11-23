from frame import Frame 
from psd_tools import PSDImage
from upload import TarmacSync

FILE_FORMAT = "img_{0}.png"

def RecursiveFrame(frame, psd, imgFrames):
	for layer in psd:
		if not layer.is_visible():
			continue

		layerFrame = Frame(layer)
		frame.AddChild(layerFrame)

		if layerFrame.instance.get("Image"):
			imgFrames.append(layerFrame)

		if layer.kind == "group":
			RecursiveFrame(layerFrame, layer, imgFrames)

def main(filename, outputPath, contentPath, cookie):
	psd = PSDImage.open(filename)
	top = Frame(psd)

	imgFrames = []
	RecursiveFrame(top, psd, imgFrames)

	for i in range(len(imgFrames)):
		name = FILE_FORMAT.format(i + 1)
		imgPath = outputPath.as_posix() + "/" + name
		imgFrames[i].layer.composite().save(imgPath)

		if contentPath:
			subPath = "/".join(contentPath.parts[-2:])
			imgFrames[i].instance["Image"] = "rbxasset://" + subPath + "/" + name
			imgFrames[i].layer.composite().save(contentPath.as_posix() + "/" + name)
	
	if cookie:
		assetids = TarmacSync(outputPath, cookie)
		for i in range(len(imgFrames)):
			imgFrames[i].instance["Image"] = assetids[i]

	json = open(outputPath.as_posix() + "/output.json", "w")
	json.write(top.ToJSON())
	json.close()