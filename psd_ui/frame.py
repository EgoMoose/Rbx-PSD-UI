import json
import instances

INDENT = 4

class Frame:
	def __init__(self, layer):
		className = instances.GetClassName(layer)
		instance = getattr(instances, className)(layer)
		instance["ClassName"] = className

		self.layer = layer
		self.instance = instance
		self.children = []
	
	def AddChild(self, child):
		self.children.append(child)
	
	def ToDict(self):
		return {
			"Instance": self.instance,
			"Children": [child.ToDict() for child in self.children]
		}
	
	def ToJSON(self):
		return json.dumps(self.ToDict(), indent=INDENT)