function run(tbl)
   local timeOri = ""
    if tbl["slots"] ~= nil then
        if tbl["slots"]["time"] ~= nil then
            timeOri = tbl["slots"]["time"]["beforevalue"]
        end
    end
    local resp = ""
    if tbl["data"] ~= nil then
        if tbl["data"]["resp"] ~= nil then
            resp = tbl["data"]["resp"]
        end
    end
    local respStr = ""
    if timeOri == "" then 
    	respStr = resp
    else 
    	respStr = timeOri .. "，" .. resp
    end
    return  respStr
end