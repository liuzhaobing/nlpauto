function run(tbl)
    local dateBeforeValue = ""
    local dateAfterValue = ""
    local cnWeekday = ""
    local holidayStatus = -1
     if tbl["slots"] ~= nil then
         if tbl["slots"]["date"] ~= nil then
            dateBeforeValue = tbl["slots"]["date"]["beforevalue"]
            dateAfterValue = tbl["slots"]["date"]["value"]
         end
     end
     if tbl["data"] ~= nil then
        if tbl["data"]["data"] ~= nil then
            cnWeekday = tbl["data"]["data"]["cnWeekday"]
            holidayStatus = tbl["data"]["data"]["holidayStatus"]
        end
     end
     local resp = ""
     if tbl["data"] ~= nil then
         if tbl["data"]["resp"] ~= nil then
             resp = tbl["data"]["resp"]
         end
     end
     local dateStr = dateAfterValue
     if string.match(dateBeforeValue, "天") or string.match(dateBeforeValue, "儿") then
         dateStr = dateBeforeValue
     end
     local respStr = ""
     if cnWeekday == "星期一" then
        if holidayStatus ~= 1 then 
            respStr = dateStr .. "是" .. cnWeekday .. "，元气满满的一周开始了"
        else
            respStr = dateStr .. "是" .. cnWeekday .. "，但是不用上班哦，尽情享受您的假期吧"
        end
     elseif cnWeekday == "星期二" then
        if holidayStatus ~= 1 then 
            respStr = dateStr .. "是" .. cnWeekday .. "，祝您度过美好的一天"
        else
            respStr = dateStr .. "是" .. cnWeekday .. "，但是不用上班哦，尽情享受您的假期吧"
        end
     elseif cnWeekday == "星期三" then
        if holidayStatus ~= 1 then 
            respStr = dateStr .. "是" .. cnWeekday .. "，嘿嘿，感觉时间过的有点慢呀"
        else
            respStr = dateStr .. "是" .. cnWeekday .. "，但是不用上班哦，尽情享受您的假期吧"
        end
     elseif cnWeekday == "星期四" then
        if holidayStatus ~= 1 then 
            respStr = dateStr .. "是" .. cnWeekday .. "，你看上去有点疲惫呢，幸苦啦"
        else
            respStr = dateStr .. "是" .. cnWeekday .. "，但是不用上班哦，尽情享受您的假期吧"
        end
     elseif cnWeekday == "星期五" then
        if holidayStatus ~= 1 then 
            respStr = dateStr .. "是" .. cnWeekday .. "，是我一周里最喜欢的一天"
        else
            respStr = dateStr .. "是" .. cnWeekday .. "，但是不用上班哦，尽情享受您的假期吧"
        end
     elseif cnWeekday == "星期六" then
        if holidayStatus == 2 then 
            respStr = dateStr .. "是" .. cnWeekday .. "，你看上去有点疲惫呢，幸苦啦"
        else
            respStr = dateStr .. "是" .. cnWeekday .. "，好好地放松一下吧"
        end
     elseif cnWeekday == "星期日" then
        if holidayStatus == 2 then 
            respStr = dateStr .. "是" .. cnWeekday .. "，你看上去有点疲惫呢，幸苦啦"
        else
            respStr = dateStr .. "是" .. cnWeekday .. "，我想宅在家里哪都不去"
        end
     end
     if respStr == "" then
         respStr = resp
     end
     return  respStr
 end