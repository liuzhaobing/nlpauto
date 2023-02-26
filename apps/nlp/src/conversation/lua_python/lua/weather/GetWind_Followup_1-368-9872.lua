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
    local wind_dir = tbl["data"]["weather_data"][1]["wind_dir"]
    local wind_sc = tbl["data"]["weather_data"][1]["wind_sc"]

    if location == "" or date == "" or wind_dir == "" or wind_sc == "" then
        return
    end

    local temp = "差点把我都给吹跑了"

    if string.find(wind_sc, "1-2")  ~= nil then
        temp = "风很柔和，就像妈妈的怀抱一样"
    end

    if string.find(wind_sc, "3-4")  ~= nil then
        temp = "风有点大呢，把我的发型都给吹乱了"
    end

    if string.find(wind_sc, "4-5")  ~= nil then
        temp = "风呼呼的，把小树苗吹的摇摇晃晃的"
    end

    local wind_sc_str = string.gsub(wind_sc, "-", "到", 1)

    return location .. "，" .. date .. "，" .. wind_dir .. "，" .. wind_sc_str .. "级，" .. temp
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