function run(tbl)
    if next(tbl["slots"]) == nil then
        return "这个地方好神秘啊，我不知道在哪里，辛苦你找别人问问吧。"
    end
    
    local slots = tbl["slots"]
    for k, v in pairs(slots) do
        if k == "type" and v ~= "" then
            return ""
        end
        if string.sub(k,1,7) == "keyword" and v ~= "" then
            return ""
        end
    end
    return "这个地方好神秘啊，我不知道在哪里，辛苦你找别人问问吧。"
end