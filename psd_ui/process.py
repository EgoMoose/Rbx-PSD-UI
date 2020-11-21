from frame import Frame 
from psd_tools import PSDImage
from upload import UploadImage

FILE_FORMAT = "{0}_{1}.png"

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
		name = FILE_FORMAT.format(outputPath.stem, i + 1)
		imgPath = outputPath.as_posix() + "/" + name
		imgFrames[i].layer.composite().save(imgPath)

		if cookie:
			assetid = UploadImage(imgPath)
			# upload imgPath to site, get asset id
			# imageFrames[i].instance["Image"] = assetid

		if contentPath:
			subPath = "/".join(contentPath.parts[-2:])
			imgFrames[i].instance["Image"] = "rbxasset://" + subPath + "/" + name
			imgFrames[i].layer.composite().save(contentPath.as_posix() + "/" + name)

	json = open(outputPath.as_posix() + "/json.txt", "w")
	json.write(top.ToJSON())
	json.close()