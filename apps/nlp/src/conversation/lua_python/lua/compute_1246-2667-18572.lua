function run(tbl)
    local a = tonumber(tbl["slots"]["A"]["value"])
    local b = tonumber(tbl["slots"]["B"]["value"])

    return "结果是:"..a^b
end