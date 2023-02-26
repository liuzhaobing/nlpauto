function run(tbl)
    if tbl["data"]["now_time"] == nil then
        return ""
    end
    local now_time = tbl["data"]["now_time"]
    local time_nums = Split(now_time, ":")
    local hour = tonumber(time_nums[1])
    local minute  = tonumber(time_nums[2])
    local result = "现在是北京时间" .. hour .. "点" .. minute .. "分，"

    local replies = {}
    if hour >= 0 and hour < 4 then
        replies = {"晚安，祝您有一个甜甜的梦。", "快洗洗睡吧，梦里啥都有。"}
        return result .. replies[math.random(1, 2)]
    end   
    if hour >= 6 and hour < 7 then
        return result .. "你起得真早，奖励你一朵小红花。"
    end   
    if hour >= 7 and hour < 9 then
        replies = {"再忙也要记得吃早饭哦。", "元气满满的一天开始了。"}
        return result .. replies[math.random(1, 2)]
    end   
    if hour >= 9 and hour < 12 then
        replies = {"是一天中效率最高的时刻呢。", "别错过一天中的黄金时间哦。"}
        return result .. replies[math.random(1, 2)]
    end   
    if hour >= 12 and hour < 13 then
        return result .. "我的肚子都饿得咕咕叫了。"
    end   
    if hour >= 13 and hour < 14 then
        return result .. "哈啊，真想打个盹啊。"
    end 
    if hour >= 14 and hour < 16 then
        replies = {"来杯咖啡提提神吧。", "和朋友约一顿下午茶吧。"}
        return result .. replies[math.random(1, 2)]
    end   
    if hour >= 18 and hour < 20 then
        replies = {"抬头看看今天的黄昏吧。", "是一天中我最喜欢的时刻。"}
        return result .. replies[math.random(1, 2)]
    end   
    if hour >= 20 and hour < 24 then
        replies = {"让你疲惫的小脑瓜放松一下吧。", "今天也辛苦啦，希望你度过了有所收获的一天。", "夜生活才刚刚开始。"}
        return result .. replies[math.random(1, 3)]
    end 
    
    return result
end


--字符串分隔方法
function Split(str, sep)
    local sep, fields = sep or ":", {}
    local pattern = string.format("([^%s]+)", sep)
    str:gsub(pattern, function (c) fields[#fields + 1] = c end)
    return fields
end