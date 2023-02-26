function run(tbl)
	local position = ""
    if tbl["slots"] ~= nil then
        if tbl["slots"]["position"] ~= nil then
            position = tbl["slots"]["position"]["value"]
        end
    end
    
    if position == "大门" then
    	return "好的，京京这就前往大门"
    elseif position == "前台" then
    	return "好的，我在旁边等您哦"
    elseif position == "3D全息投影" then
        return "好的，我们出发吧"
    elseif position == "区位图" then
        return "好的，请随我来吧"
    elseif position == "迎宾点" then
    	return "好的，京京这就前往迎宾点"
    elseif string.sub(position,1,9) == "装载点" then
    	return "好的，京京这就去"
    else
    	return
    end
    return 
end