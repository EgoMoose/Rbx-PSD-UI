import json
import instances

INDENT = 4

class Frame:
	def __init__(self, layer):
		classname = instances.GetClassName(layer)
		instance = getattr(instances, classname)(layer)

		self.layer = layer
		self.classname = classname
		self.instance = instance
		self.children = []
	
	def AddChild(self, child):
		self.children.append(child)
	
	def ToDict(self):
		return {
			"Instance": self.instance,
			"ClassName": self.classname,
			"Children": [child.ToDict() for child in self.children]
		}
	
	def ToJSON(self):
		return json.dumps(self.ToDict(), indent=INDENT)