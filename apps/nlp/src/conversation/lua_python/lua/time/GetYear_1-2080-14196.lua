function run(tbl)
   local yearBeforeValue = ""
   local yearAfterValue = ""
   local ganzhi = ""
   local zodiac = ""
   local zodiacParam = ""
   local orientation = ""
   local zodiacYearStr = ""
   if tbl["slots"] ~= nil then
      if tbl["slots"]["year"] ~= nil then
         yearBeforeValue = tbl["slots"]["year"]["beforevalue"]
         yearAfterValue = tbl["slots"]["year"]["value"]
      end
      if tbl["slots"]["number"] ~= nil and yearBeforeValue == "" then
         yearBeforeValue = tbl["slots"]["number"]["beforevalue"]
         yearAfterValue = tbl["slots"]["number"]["value"]
      end
   end
   if tbl["data"] ~= nil then
      if tbl["data"]["data"] ~= nil then
         ganzhi = tbl["data"]["data"]["ganZhi"]
         zodiac = tbl["data"]["data"]["zodiac"]
         zodiacParam = tbl["data"]["data"]["zodiacParam"]
         orientation = tbl["data"]["data"]["orientation"]
         zodiacYearStr = tbl["data"]["data"]["zodiacYearStr"]
      end
   end
   local resp = ""
   local respStr = ""
   if tbl["data"] ~= nil then
      if tbl["data"]["resp"] ~= nil then
         resp = tbl["data"]["resp"]
      end
   end
   if orientation ~= "" and zodiacParam ~= "" then
      respStr = orientation .. "一个" .. zodiacParam .. "年是" .. zodiacYearStr .. "年"
   else
      local yearStr = yearAfterValue.."年"
      if string.match(yearBeforeValue, "年") then
         yearStr = yearBeforeValue
      end
      respStr = yearStr .. "是" .. ganzhi .. "，生肖为" .. zodiac
      if zodiac == "鼠" then
         respStr = respStr .. "，愿您有鼠不完的钱财滚滚来"
      elseif zodiac == "牛" then
         respStr = respStr .. "，愿您牛转乾坤逆风翻盘"
      elseif zodiac == "虎" then
         respStr = respStr .. "，愿您虎虎生威行大运"
      elseif zodiac == "兔" then
         respStr = respStr .. "，愿您兔气扬眉神奇一整年"
      elseif zodiac == "龙" then
         respStr = respStr .. "，愿您龙马精神好运来"
      elseif zodiac == "蛇" then
         respStr = respStr .. "，愿您金蛇狂舞步步高"
      elseif zodiac == "马" then
         respStr = respStr .. "，愿您一路高歌马到成功"
      elseif zodiac == "羊" then
         respStr = respStr .. "，愿您羊羊得意乐开怀"
      elseif zodiac == "猴" then
         respStr = respStr .. "，愿您猴来居上旗开得胜"
      elseif zodiac == "鸡" then
         respStr = respStr .. "，愿您大鸡大利行大运"
      elseif zodiac == "狗" then
         respStr = respStr .. "，愿您十犬十美好运连连"
      elseif zodiac == "猪" then
         respStr = respStr .. "，愿您猪事如意发大财"
      end
   end
   if respStr == "" then
      respStr = resp
   end
   return respStr
end