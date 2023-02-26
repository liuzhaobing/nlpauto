function run(tbl)
    local stock_id = ""
    if tbl["slots"] ~= nil then
        if tbl["slots"]["stockid"] ~= nil then
            stock_id = tbl["slots"]["stockid"]["value"]
        end
    end
    if stock_id == "" then
        return
    end

    local first = string.sub(stock_id, 1, 2)
    local stock_type = ""
    local currency = ""
    if first == "sh" or first == "sz" then
        stock_type = "hs"
        currency = "元"
    end
    first = string.sub(stock_id, 1, 1)
    if first >= "0" and first <= "9" then
        stock_type = "hk"
        currency = "港元"
    end
    if first >= "A" and first <= "Z" then
        stock_type = "usa"
        currency = "美元"
    end
    local is_today = false
    local is_close = false
    local stock_name = tbl["data"]["name"]
    local now_pri = tbl["data"]["nowPri"]
    local incre_per = tbl["data"]["increPer"]
    local yes_pri = tbl["data"]["yestodEndPri"]
    local time = tbl["data"]["time"]

    local today_date = ""
    if stock_type == "hk" then
        today_date = os.date("%Y/%m/%d")
    elseif stock_type == "usa" then
        today_date = os.date("%Y-%m-%d")
    else
        today_date = os.date("%Y-%m-%d")
    end

    if split(time, " ")[1] == today_date then
        is_today = true
    end

    local time2 = os.date("%H:%M:%S")
    local _, _, h, m, s = string.find(split(time, " ")[2], "(%d+):(%d+):(%d+)")
    local _, _, h2, m2, s2 = string.find(time2, "(%d+):(%d+):(%d+)")
    --转化为时间戳
    local t1 = os.time({year=2022, month = 01, day = 26, hour = tonumber(h), min = tonumber(m), sec = tonumber(s)})
    local t2 = os.time({year=2022, month = 01, day = 26, hour = tonumber(h2), min = tonumber(m2), sec = tonumber(s2)})
    if stock_type == "" or stock_type == "hs" then
        if (t2 - t1) / 60 > 5 and time > "15:00:00" then
            is_close = true
        end
    elseif stock_type == "hk" then
        if (t2 - t1) / 60 > 5 and time > "16:00:00" then
            is_close = true
        end
    elseif stock_type == "usa" then
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
        return "今日未开盘，" .. stock_name .. "上个交易日价格" .. now_pri .. currency .. "，" .. up_down .. "。"
    elseif is_close then
        return stock_name .. "当前价格" .. now_pri .. currency .. "，" .. up_down .. "，已收盘。"
    else 
        return stock_name .. "当前价格" .. now_pri .. currency .. "，" .. up_down .. "。"
    end
end

--字符串分隔方法
function split(str, sep)
    local sep, fields = sep or ":", {}
    local pattern = string.format("([^%s]+)", sep)
    str:gsub(pattern, function (c) fields[#fields + 1] = c end)
    return fields
end 