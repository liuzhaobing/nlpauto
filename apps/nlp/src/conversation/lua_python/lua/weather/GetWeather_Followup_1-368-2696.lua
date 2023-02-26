function run(tbl)
    if tbl["slots"] ~= nil and tbl["params"] ~=nil then
        if tbl["slots"]["country"] ~= nil and tbl["params"]["Default"] ~= nil and string.find(tbl["params"]["Default"], tbl["slots"]["country"]["beforevalue"]) ~= nil then
            if tbl["slots"]["city"] == nil or (tbl["slots"]["city"] ~= nil and string.find(tbl["params"]["Default"], tbl["slots"]["city"]["beforevalue"])==nil) then
                return "这个范围太大了呢，请告诉我具体是哪个城市吧！"
            end
        end
    end
    local days = #(tbl["data"]["weather_data"])
    if days > 1 and days <= 7 then
        local result = tbl["data"]["location"] .. ", "
        for i,weather in ipairs(tbl["data"]["weather_data"]) do
            local fields = split(weather["date"], "-")
            local date = fields[2] .. "月" .. fields[3] .. "日"
            local cond_txt_d = weather["cond_txt_d"]
            local cond_txt_n = weather["cond_txt_n"]
            local tmp_min = weather["tmp_min"]
            local tmp_max = weather["tmp_max"]

            local tmp_min_str = tmp_min
            local tmp_max_str = tmp_max
            if string.find(tmp_min, "-") ~= nil then
                tmp_min_str = "零下" .. string.sub(tmp_min, 2)
            end
            if string.find(tmp_max, "-") ~= nil then
                tmp_max_str = "零下" .. string.sub(tmp_max, 2)
            end  
            if cond_txt_d == cond_txt_n then
                result = result .. date .. "，" .. cond_txt_d .. "，" .. tmp_min_str .. "至" .. tmp_max_str .. "度" .. "；"
            else 
                result = result .. date .. "，" .. cond_txt_d .. "转" .. cond_txt_n .. "，" .. tmp_min_str .. "至" .. tmp_max_str .. "度" .. "；"
            end
        end
        result = result .. "若想了解更多，也可具体询问我某一天的天气哦。"  
        return result
    end

    if days >  7 then
        local result = tbl["data"]["location"]
        local min_sum = 0
        local max_sum = 0
        local cond_table = {}
        cond_table["晴天"] = 0
        cond_table["多云"] = 0
        cond_table["阴天"] = 0
        cond_table["降雨"] = 0
        cond_table["降雪"] = 0
        local temp_table = {}
        temp_table["hot"] = 0
        temp_table["cold"] = 0
        for i,weather in ipairs(tbl["data"]["weather_data"]) do
            local date = string.sub(weather["date"], 6)
            local cond_txt_d = weather["cond_txt_d"]
            local cond_txt_n = weather["cond_txt_n"]
            local tmp_min = weather["tmp_min"]
            local tmp_max = weather["tmp_max"]

            min_sum = min_sum + tonumber(tmp_min)
            max_sum = max_sum + tonumber(tmp_max)

            if string.find(cond_txt_d, "晴") ~= nil then
                cond_table["晴天"] = cond_table["晴天"] + 1
            end
            if string.find(cond_txt_d, "多云") ~= nil then
                cond_table["多云"] = cond_table["多云"] + 1
            end
            if string.find(cond_txt_d, "阴") ~= nil then
                cond_table["阴天"] = cond_table["阴天"] + 1
            end
            if string.find(cond_txt_d, "雨") ~= nil then
                cond_table["降雨"] = cond_table["降雨"] + 1
            end
            if string.find(cond_txt_d, "雪") ~= nil then
                cond_table["降雪"] = cond_table["降雪"] + 1
            end

            if tonumber(tmp_min) >= 27 then
                temp_table["hot"] = temp_table["hot"] + 1
            end 
            if tonumber(tmp_max) <= 5 then
                temp_table["cold"] = temp_table["cold"] + 1
            end 
        end

        result = result .. "未来一周， "  
        min_avg = math.floor(min_sum / days + 0.5)
        max_avg = math.floor(max_sum / days + 0.5)
        local tmp_min_str = tostring(min_avg) .. "度，"
        local tmp_max_str = tostring(max_avg) .. "度，"
        if min_avg < 0 then
            tmp_min_str = "零下" .. string.sub(tmp_min_str, 2) 
        end
        if max_avg < 0 then
            tmp_max_str = "零下" .. string.sub(tmp_max_str, 2)
        end
        for cond, num in pairs(cond_table) do
            if num >= 4 then
                return result .. "以" .. cond .. "为主，" .. "平均最低温" .. tmp_min_str  ..  "平均最高温" .. tmp_max_str ..  "若想了解更多，也可具体询问我某一天的天气哦。" 
            end
        end

        if temp_table["hot"] >= 4 then
            return result .. "以热的冒烟模式为主，" .. "平均最低温" .. tmp_min_str .. "平均最高温" .. tmp_max_str ..  "若想了解更多，也可具体询问我某一天的天气哦。" 
        end
        if temp_table["cold"] >= 4 then
            return result .. "以冷的发抖模式为主，" .. "平均最低温" .. tmp_min_str .. "平均最高温" .. tmp_max_str ..  "若想了解更多，也可具体询问我某一天的天气哦。" 
        end

        if max_avg - min_avg > 10 then
            return result .. "温差较大，" .. "平均最低温" .. tmp_min_str .. "平均最高温" .. tmp_max_str ..  "若想了解更多，也可具体询问我某一天的天气哦。" 
        end
        
        return result .. "平均最低温" .. tmp_min_str .. "平均最高温" .. tmp_max_str ..  "若想了解更多，也可具体询问我某一天的天气哦。" 
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
    local wind_sc = tbl["data"]["weather_data"][1]["wind_sc"]
    local uv_index = tbl["data"]["weather_data"][1]["uv_index"]

    if tbl["slots"] ~= nil then
        if tbl["slots"]["city"] ~= nil then
            location = tbl["slots"]["city"]["beforevalue"]
        end
    end

    if location == "" or date == "" or cond_txt_d == "" or cond_txt_n == "" or tmp_min == "" or tmp_max == "" then
        return
    end

    local tmp_min_str = tmp_min
    local tmp_max_str = tmp_max

    if string.find(tmp_min, "-") ~= nil then
        tmp_min_str = "零下" .. string.sub(tmp_min, 2)
    end

    if string.find(tmp_max, "-") ~= nil then
        tmp_max_str = "零下" .. string.sub(tmp_max, 2)
    end

    temp1 = location .. "，" .. date .. "天气" .. cond_txt_d .. "，" .. tmp_min_str .. "至" .. tmp_max_str .. "度" .. "，"
    if cond_txt_d ~= cond_txt_n then
        temp1 = location .. "，" .. date .. "天气" .. cond_txt_d .. "转" .. cond_txt_n .. "，" .. tmp_min_str .. "至" .. tmp_max_str .. "度" .. "，"
    end

    local temp2 = {}
    
    if string.find(cond_txt_d .. cond_txt_n, "雨") ~= nil then
        temp2 = {"出门记得带把伞哦", "这两天就别洗车咯", "穿双防水的鞋吧"}
        return temp1 .. temp2[math.random(1, 3)]
    end

    if string.find(cond_txt_d .. cond_txt_n, "雪") ~= nil then
        temp2 = {"出门记得带双手套", "出门记得穿双防滑的鞋", "叫上朋友来家吃火锅吧"}
        return temp1 .. "" .. temp2[math.random(1, 3)]
    end

    if tonumber(split(wind_sc,"-")[2]) >= 7 then
        temp2 = {"外面风呼呼的，请尽量减少外出", "外面风超大，你可小心别被吹跑了。"}
        return temp1 .. temp2[math.random(1, 2)]
    end

    local tmp_min_num = tonumber(tmp_min)
    local tmp_max_num = tonumber(tmp_max)

    if tmp_min_num < 0 then
        temp2 = {"别在室外呆太久哦，小心冻成冰棍", "出门的话建议您随身带片暖宝宝"}
        return temp1 .. temp2[math.random(1, 2)]
    end
    if tmp_min_num >= 0 and tmp_min_num < 8 then
        temp2 = {"天气寒冷，请注意保暖", "若不穿秋裤，后果请自负"}
        return temp1 .. temp2[math.random(1, 2)]
    end
    if tmp_max_num >= 8 and tmp_max_num < 15 then
        local wind_sc_num = tonumber(split(wind_sc,"-")[2])
        if wind_sc_num >= 1 and wind_sc_num <= 4 then
            temp2 = {"天气变化多端，注意别感冒啦", "很适合来一杯香甜的热拿铁呢"}
            return temp1 .. temp2[math.random(1, 2)]
        end

        if wind_sc_num >= 5 then
            temp2 = {"穿件酷酷的风衣出门吧", "外面妖风阵阵，记得添加衣物哦"}
            return temp1 .. temp2[math.random(1, 2)]
        end
    end
    if tmp_max_num >= 15 and tmp_max_num < 23 then
        temp2 = {"很适合出门夜跑呢", "温度适宜，适合外出游玩"}
        return temp1 .. temp2[math.random(1, 2)]
    end
    if tmp_max_num >= 23 and tmp_max_num < 30 then
        temp2 = {"约上朋友出去野个餐吧", "切记不要贪凉，感冒了我会心疼的"}
        return temp1 .. temp2[math.random(1, 2)]
    end
    if tmp_max_num >= 30 and tonumber(uv_index) > 5 then
        temp2 = {"紫外线强烈注意防晒哦", "紫外线强烈戴顶帽子出门吧"}
        return temp1 .. temp2[math.random(1, 2)]
    end
    if tmp_max_num >= 30 and tonumber(uv_index) <= 5 then
        temp2 = {"天热记得多多补充水分哦", "天气闷热穿件透气的衬衣吧"}
        return temp1 .. temp2[math.random(1, 2)]
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

--字符串分隔方法
function split(str, sep)
    local sep, fields = sep or ":", {}
    local pattern = string.format("([^%s]+)", sep)
    str:gsub(pattern, function (c) fields[#fields + 1] = c end)
    return fields
end