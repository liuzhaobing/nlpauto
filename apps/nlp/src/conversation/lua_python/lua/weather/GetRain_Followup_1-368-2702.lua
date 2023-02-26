function run(tbl)
    if #(tbl["data"]["weather_data"]) > 1 then
        return ""
    end

    local date = ""
    if tbl["slots"] ~= nil then
        if tbl["slots"]["date"] ~= nil then
            date = tbl["slots"]["date"]["beforevalue"]
        end
    end
    if tbl["slots"] ~= nil then
        if tbl["slots"]["period"] ~= nil then
            date = tbl["slots"]["period"]["beforevalue"]
        end
    end
    if date == nil or date == "" then    
        date = convertDate(tbl["data"]["weather_data"][1]["date"])
    end

    local location = tbl["data"]["location"]
    local cond_txt_d = tbl["data"]["weather_data"][1]["cond_txt_d"]
    local cond_txt_n = tbl["data"]["weather_data"][1]["cond_txt_n"]
    local tmp_min = tbl["data"]["weather_data"][1]["tmp_min"]
    local tmp_max = tbl["data"]["weather_data"][1]["tmp_max"]

    if location == "" or date == "" or cond_txt_d == "" or cond_txt_n == "" or tmp_min == "" or tmp_max == "" then
        return
    end

    if string.find(tmp_min, "-") ~= nil then
        tmp_min = "零下" .. string.sub(tmp_min, 2)
    end

    if string.find(tmp_max, "-") then
        tmp_max = "零下" .. string.sub(tmp_max, 2)
    end

    local temp1 = location .. "，" .. date .. "，"
    
    if string.find(cond_txt_d .. cond_txt_n, "雨") == nil then
        local temp2 = {"放心出门玩吧", "别宅在家里了，出门走走吧"}
        return temp1 .. "没有雨，" .. tmp_min .. "至" .. tmp_max .. "度，" .. temp2[math.random(1, 2)]
    end

    local cond_txt = cond_txt_d
    if cond_txt_d ~= cond_txt_n then
        cond_txt = cond_txt_d .. "转" .. cond_txt_n
    end
    if string.find(cond_txt_d .. cond_txt_n, "雨") ~= nil then
        temp2 = {"出门记得带把伞哦", "这两天就别洗车咯", "穿双防水的鞋吧", "我都快发霉了"}
        return temp1 .. cond_txt .. "，" .. tmp_min .. "至" .. tmp_max .. "度，" .. temp2[math.random(1, 4)]
    end
    
    return temp1 .. cond_txt .. "，" .. tmp_min .. "至" .. tmp_max .. "度"
end


function convertDate(date)
    local HOUR_OF_DAY = 24
    local SECOND_OF_HOUR = 3600
    local SECOND_OF_DAY = HOUR_OF_DAY * SECOND_OF_HOUR
    if date == nil or date == "" then
        return ""
    end

    local _, _, y, m, d = string.find(date, "(%d+)-(%d+)-(%d+)")
    local dateTime = os.time({year=tonumber(y), month=tonumber(m), day=tonumber(d), hour=23, min=59, sec=59})
    local nowTime = os.time()
    local intervalDays = math.floor((dateTime - nowTime) / SECOND_OF_DAY)

    if intervalDays == 0 then
        return "今天"
    end

    if intervalDays == 1 then
        return "明天"
    end

    if intervalDays == 2 then
        return "后天"
    end

    return date
end