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
    local uv_index_str = tbl["data"]["weather_data"][1]["uv_index"]

    if location == "" or date == "" or uv_index_str == "" then
        return
    end

    local temp = ""
    local uv_index = tonumber(uv_index_str)

    if uv_index >= 0 and uv_index <= 2 then
        temp = "极弱，估计是太阳公公休假去了吧"
    elseif uv_index >= 3 and uv_index <= 4 then
        temp = "较弱，阳光都被乌云遮住啦"
    elseif uv_index >= 5 and uv_index <= 6 then
        temp = "较强，出门前记得涂点防晒霜哦"
    elseif uv_index >= 7 and uv_index <= 9  then
        temp = "蛮强的，请做好充足的防晒措施，避免阳光直晒"
    elseif uv_index >= 10 then
        temp = "超级强，请尽可能地待在阴凉处，晒伤了我会心疼的"
    end

    return location .. "，" .. date .. "紫外线指数为" .. uv_index_str .. "，" .. temp
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