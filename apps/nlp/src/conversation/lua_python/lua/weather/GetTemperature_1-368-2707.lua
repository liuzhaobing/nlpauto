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
    local tmp_min = tbl["data"]["weather_data"][1]["tmp_min"]
    local tmp_max = tbl["data"]["weather_data"][1]["tmp_max"]

    if location == "" or date == "" or tmp_min == "" or tmp_max == "" then
        return
    end

    local tmp_min_str = tmp_min
    local tmp_max_str = tmp_max

    if string.find(tmp_min, "-") ~= nil then
        tmp_min_str = "零下" .. string.sub(tmp_min, 2)
    end

    if string.find(tmp_max, "-")  ~= nil then
        tmp_max_str = "零下" .. string.sub(tmp_max, 2)
    end

    local temp1 = location .. "，" .. date .. "，"
    local temp2 = tmp_min_str .. "至" .. tmp_max_str .. "度，"
    local temp3 = {}

    local tmp_min_num = tonumber(tmp_min)
    local tmp_max_num = tonumber(tmp_max)

    if tmp_min_num < 0 then
        temp3 = {"把我都给冻傻了", "你可别在室外呆太久哦"}
        return temp1 .. "冷的跟冰窟窿一样，" .. temp2 .. temp3[math.random(1, 2)]
    end
    if tmp_min_num >= 0 and tmp_min_num < 8 then
        temp3 = {"记得穿秋裤哦", "请多喝热水，注意保暖"}
        return temp1 .. "天气寒冷， " .. temp2 .. temp3[math.random(1, 2)]
    end
    if tmp_max_num >= 8 and tmp_max_num < 15 then
        temp3 = {"带条围巾出门吧", "很适合在被窝里睡懒觉"}
        return temp1 .. "冷飕飕的，" .. temp2 .. temp3[math.random(1, 2)]
    end
    if tmp_max_num >= 15 and tmp_max_num < 23 then
        temp3 = {"约上朋友出去野餐吧", "超级适合出门夜跑呢"}
        return temp1 .. "温度适宜，" .. temp2 .. temp3[math.random(1, 2)]
    end
    if tmp_max_num >= 23 and tmp_max_num < 30 then
        temp3 = {"穿件透气的衬衣是不错的选择", "切记不要贪凉，感冒了我会心疼的"}
        return temp1 .. "有一丢丢热，" .. temp2 .. temp3[math.random(1, 2)]
    end
    if tmp_max_num >= 30 then
        temp3 = {"请及时补充水分哦", "注意防晒哦，晒伤了我会心疼的"}
        return temp1 .. "热得跟火炉一样，" .. temp2 .. temp3[math.random(1, 2)]
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