# These functions are used to define the values of properties we'll need
# for the actual Roblox instances. Any special processing cases can be added here

import re

CLASS_NAMES = {
	"psdimage": "Frame",
	"group": "Frame",
	"type": "TextLabel",
}

FLAG_CLASS_NAMES = {
	"TEXT_": "TextLabel",
}

FLAG_FUNCTIONS = {
	"TEXT_": "RasterizedTextLabel",
}

def GetClassName(layer):
	for key in FLAG_CLASS_NAMES:
		if layer.name[:len(key)] == key:
			return FLAG_CLASS_NAMES.get(key)
	return CLASS_NAMES.get(layer.kind, "ImageLabel")

def GetClassFunc(layer):
	for key in FLAG_FUNCTIONS:
		if layer.name[:len(key)] == key:
			return FLAG_FUNCTIONS.get(key)
	return CLASS_NAMES.get(layer.kind, "ImageLabel")

# Non-flagged instances

def Frame(layer):
	offset = layer.offset

	if layer.parent:
		x1, y1 = offset[0], offset[1]
		x2, y2 = layer.parent.offset[0], layer.parent.offset[1]
		offset = (x1 - x2, y1 - y2)
	
	return {
		"Name": layer.name,
		"Size": layer.size,
		"Position": offset,
		"BackgroundTransparency": 1
	}

def ImageLabel(layer):
	instance = Frame(layer)
	instance["Image"] = True # This is set later, but for now we use as a flag that the instance has an image
	return instance

def TextLabel(layer):
	style = layer.engine_dict['StyleRun']['RunArray'][0]["StyleSheet"]["StyleSheetData"]

	fillColor = style["FillColor"]["Values"]
	strokeColor = style["StrokeColor"]["Values"]

	instance = Frame(layer)
	instance["Text"] = layer.text
	instance["TextSize"] = int(style["FontSize"])
	instance["TextColor3"] = ", ".join(map(str, [fillColor[1], fillColor[2], fillColor[3]]))
	instance["TextStrokeColor3"] = ", ".join(map(str, [strokeColor[1], strokeColor[2], strokeColor[3]]))
	instance["TextTransparency"] = str(1 - fillColor[0])

	return instance


# Flagged instances

def RasterizedTextLabel(layer):
	instance = Frame(layer)
	instance["Name"] = layer.name[5:]
	instance["Text"] = "TextLabel"
	return instance