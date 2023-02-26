function run(tbl)
    local holiday = ""
    local status = -1
    local dateStr = ""
    local dateBefore = ""
     if tbl["slots"] ~= nil then
         if tbl["slots"]["date"] ~= nil then
            dateBefore = tbl["slots"]["date"]["beforevalue"]
         end
     end
     if tbl["data"] ~= nil then
        if tbl["data"]["data"] ~= nil then
            dateStr = tbl["data"]["data"]["dateStr"]
            status = tbl["data"]["data"]["status"]
            holiday = tbl["data"]["data"]["holidayStr"]
        end
     end
     local resp = ""
     if tbl["data"] ~= nil then
         if tbl["data"]["resp"] ~= nil then
             resp = tbl["data"]["resp"]
         end
     end
     if string.match(dateBefore, "天") then
        dateStr = dateBefore
     end
     local respStr = ""
     if status==1 then
        respStr = dateStr .. "，是工作日，请您专心搬砖，假期总会到来的。"
     elseif status==2 then
        respStr = dateStr .. "，是周末，祝你拥有一个愉快的周末。"
     elseif status==3 then
        respStr = dateStr .. "，正值"..holiday.."假期，祝你拥有一个愉快的假期。"
     elseif status==4 then
        respStr = dateStr .. "，是"..holiday.."的调休日，仍然需要上班，辛苦了。"
     end
     if holiday=="三八妇女节" then
        respStr = dateStr .. "是"..holiday.."，妇女放假半天"
     elseif holiday=="青年节" then
        respStr = dateStr .. "是"..holiday.."，14岁以上的青年放假半天"
     elseif holiday=="儿童节" then
        respStr = dateStr .. "是"..holiday.."，不满14周岁的少年儿童放假1天"
     elseif holiday=="建军节" then
        respStr = dateStr .. "是"..holiday.."，现役军人放假半天"
     end
     if respStr == "" then
         respStr = resp
     end
     return  respStr
 end