function run(tbl)
    local dateBefore = ""
    local dateStr = ""
    local lunarStr = ""
    local suitStr = ""
    local avoidStr = ""
     if tbl["slots"] ~= nil then
         if tbl["slots"]["date"] ~= nil then
            dateBefore = tbl["slots"]["date"]["beforevalue"]
         end
     end
     if tbl["data"] ~= nil then
        if tbl["data"]["data"] ~= nil then
            dateStr = tbl["data"]["data"]["date"]
            lunarStr = tbl["data"]["data"]["lunarStr"]
            suitStr = tbl["data"]["data"]["suitStr"]
            avoidStr = tbl["data"]["data"]["avoidStr"]
        end
     end
     local resp = ""
     if tbl["data"] ~= nil then
         if tbl["data"]["resp"] ~= nil then
             resp = tbl["data"]["resp"]
         end
     end
     if string.match(dateBefore, "天") or string.match(dateBefore, "儿") then
        dateStr = dateBefore
     end
     local respStr = dateStr.. "是农历"..lunarStr.."，宜："..suitStr.."；忌："..avoidStr
     if respStr == "" then
         respStr = resp
     end
     return  respStr
 end