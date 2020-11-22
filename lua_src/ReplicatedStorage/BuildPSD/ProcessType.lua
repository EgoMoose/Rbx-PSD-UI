local function udim2(arr)
	return UDim2.new(0, arr[1], 0, arr[2])
end

local function color3(str)
	local arr = {}
	for match in string.gmatch(str, "%-*%d[%d.]*") do
		arr[#arr + 1] = match
	end
	return Color3.new(unpack(arr))
end

local module = {}

module.Position = udim2
module.Size = udim2
module.TextColor3 = color3
module.TextStrokeColor3 = color3
module.TextSize = tonumber

return module