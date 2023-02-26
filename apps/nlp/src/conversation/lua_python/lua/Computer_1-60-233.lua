function run(tbl)
    local query = ""
     if tbl["params"] ~= nil then
         query = tbl["params"]["query"]
     end
     local resp = ""
     if tbl["slots"] ~= nil then
         if tbl["slots"]["compute"] ~= nil then
             resp = tbl["slots"]["compute"]["value"]
         end
     end
     local respStr = ""
     if string.find(query,"分之") then
             respStr = "告诉你个秘密，我的数学是体育老师教的"
     else
            respStr = "等于" .. resp
     end
     return  respStr
 end