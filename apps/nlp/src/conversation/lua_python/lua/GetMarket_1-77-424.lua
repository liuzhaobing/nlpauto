function run(tbl)
    local stock_index = ""
    if tbl["slots"] ~= nil then
        if tbl["slots"]["stock_index"] ~= nil then
            stock_index = tbl["slots"]["stock_index"]["value"]
        end
    end
    local index_name = ""
    if stock_index == "" or stock_index == "sh" then
        index_name = "上证指数"
    end
    if stock_index == "sz" then
        index_name = "深证成指"
    end
    if stock_index == "hk" then
        index_name = "恒生指数"
    end
    if stock_index == "usa" then
        index_name = "纳斯达克指数"
    end
    local is_today = false
    local is_close = false
    local now_pri = tbl["data"]["nowPri"]
    local incre_per = tbl["data"]["increPer"]
    local yes_pri = tbl["data"]["yesPri"]
    local date = tbl["data"]["date"]
    local time = tbl["data"]["time"]
    if stock_index == "usa" then
        date = split(time, " ")[1]
        time = split(time, " ")[2]
    end
    local today_date = ""
    if stock_index == "hk" then
        today_date = os.date("%Y/%m/%d")
    elseif stock_index == "usa" then
        today_date = os.date("%Y-%m-%d")
    else
        today_date = os.date("%Y-%m-%d")
    end
    
    if date == today_date then
        is_today = true
    end

    local time2 = os.date("%H:%M:%S")
    local _, _, h, m, s = string.find(time, "(%d+):(%d+):(%d+)")
    local _, _, h2, m2, s2 = string.find(time2, "(%d+):(%d+):(%d+)")
    --转化为时间戳
    local t1 = os.time({year=2022, month = 01, day = 26, hour = tonumber(h), min = tonumber(m), sec = tonumber(s)})
    local t2 = os.time({year=2022, month = 01, day = 26, hour = tonumber(h2), min = tonumber(m2), sec = tonumber(s2)})
    if stock_index == "" or stock_index == "sh" or stock_index == "sz" then
        if (t2 - t1) / 60 > 5 and time > "15:00:00" then
            is_close = true
        end
    elseif stock_index == "hk" then
        if (t2 - t1) / 60 > 5 and time > "16:00:00" then
            is_close = true
        end
    elseif stock_index == "usa" then
        if time > "04:00:00" and time < "21:30:00" then
            is_close = true
        end
    end
    local percent = tonumber(incre_per)
    local up_down = ""
    if string.find(incre_per, "-") ~= nil then
        up_down = "跌幅" .. string.sub(incre_per, 2) .. "%"
    elseif percent == 0 then
        up_down = "无涨跌"
    else 
        up_down = "涨幅" .. incre_per .. "%"
    end

    if not is_today then
        return "今日未开盘，" .. index_name .. "上个交易日价格" .. now_pri .. "点，" .. up_down .. "。"
    elseif is_close then
        return index_name .. "当前价格" .. now_pri .. "点，" .. up_down .. "，已收盘。"
    else 
        return index_name .. "当前价格" .. now_pri .. "点，" .. up_down .. "。"
    end
end

--字符串分隔方法
function split(str, sep)
    local sep, fields = sep or ":", {}
    local pattern = string.format("([^%s]+)", sep)
    str:gsub(pattern, function (c) fields[#fields + 1] = c end)
    return fields
end 