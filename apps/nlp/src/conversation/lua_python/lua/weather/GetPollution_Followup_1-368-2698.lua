function run(tbl)
    local location = tbl["data"]["location"]
    local aqi = tonumber(tbl["data"]["aqi"])
    if aqi == nil then
        if tbl["data"]["air_forecast"] ~= nil then
            if #(tbl["data"]["air_forecast"]) > 1 then
                return ""
            end
            aqi = tonumber(tbl["data"]["air_forecast"][1]["aqi"])
        end
    end
    if aqi == nil then
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
    local pub_time = tbl["data"]["pub_time"]
    if date == nil or date == "" then    
        date = convertDate(string.sub(pub_time, 1, 10))
    end

    if location == "" or aqi == "" or pub_time == "" or date == "" then
        return
    end

    local temp1 = location .. "，" .. date .. "，" .. "空气质量指数" .. aqi
    local temp2 = {}

    if aqi >= 0 and aqi <= 50 then
        temp2 = {"空气很好", "空气很清新"}
        return temp1 .. "，" .. temp2[math.random(1, 2)] .. "，尽情享受户外活动吧"
    end
    if aqi >= 51 and aqi <= 100 then
        temp2 = {"空气良好", "空气还不错"}
        return temp1 .. "，" .. temp2[math.random(1, 2)] .. "，出门散散步吧"
    end
    if aqi >= 101 and aqi <= 150 then
        temp2 = {"空气轻度污染", "空气有点脏脏的呢"}
        return temp1 .. "，" .. temp2[math.random(1, 2)] .. "，请尽量减少外出"
    end
    if aqi >= 151 and aqi <= 200 then
        temp2 = {"空气中度污染", "空气比较差"}
        return temp1 .. "，" .. temp2[math.random(1, 2)] .. "，不要在户外进行高强度的运动哦"
    end
    if aqi >= 201 and aqi <= 300 then
        temp2 = {"空气脏的让人窒息", "空气很差"}
        return temp1 .. "，" .. temp2[math.random(1, 2)] .. "，出门一定要带口罩啊"
    end
    if aqi > 300 then
        temp2 = {"空气严重污染", "空气污染爆表啦"}
        return temp1 .. "，" .. temp2[math.random(1, 2)] .. "，乖乖待在屋子里吧"
    end
    
    return temp1
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