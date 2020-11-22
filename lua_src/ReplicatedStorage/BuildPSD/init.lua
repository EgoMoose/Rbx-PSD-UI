local HttpService = game:GetService("HttpService")
local StarterGui = game:GetService("StarterGui")

local ProcessType = require(script:WaitForChild("ProcessType"))

local function make(layer)
	local frame = Instance.new(layer.ClassName)
	for property, value in pairs(layer.Instance) do
		if ProcessType[property] then
			value = ProcessType[property](value)
		end
		frame[property] = value
	end
	return frame
end

local function makeAll(layer, parent)
	local frame = make(layer)
	for _, child in pairs(layer.Children) do
		makeAll(child, frame)
	end
	frame.Parent = parent
	return frame
end

local function build(json)
	local top = HttpService:JSONDecode(json)
	local screen = Instance.new("ScreenGui")
	local container = makeAll(top, screen)
	container.ClipsDescendants = true
	screen.Parent = StarterGui
end

return build