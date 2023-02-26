import json
import random

topic_list = [
    {"id": 3852, "title": "坐进观天",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/131923/qfkErqOC.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=F%2FFufzthnVRX5LERY6xcfByGrtM%3D"},
    {"id": 3851, "title": "左顾右盼",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/131903/o8wi7kts.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=GgdsoWQ96rl7HEEzL3eLbq3soDA%3D"},
    {"id": 3850, "title": "自圆其说",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/131842/CNMwlBSM.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=hiiOuLPC06G35Hpd0ulTL1yI9eA%3D"},
    {"id": 3849, "title": "紫气东来",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/131817/YqjJUHiA.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=yB9pZ75vR3ozqBhXX%2F4%2Ficzonzo%3D"},
    {"id": 3848, "title": "支离破碎",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/131757/xLNfG86H.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=RLmL6fLy8%2BTLsW3%2F9BRIMQwyWiE%3D"},
    {"id": 3847, "title": "正中下怀",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/131730/wDgcCrnh.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=lk5ZKfwbtt%2BDTvoIQKmb7cEvmFc%3D"},
    {"id": 3846, "title": "针锋相对",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/131705/xuTtyNpu.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=z70sodSldHtaZSC7UVft6ahnKz0%3D"},
    {"id": 3845, "title": "长话短说",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/131642/PcCnaKfv.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=wxR7Z5bkm8Q5kQjgDjtWJfGRMvI%3D"},
    {"id": 3844, "title": "异曲同工",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/131611/ruchUqKx.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=WmQYskBEhFplMd4H1TFhtRP0Dag%3D"},
    {"id": 3843, "title": "衣食父母",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/131535/MtPLqY0G.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=qkUj%2FGyoKEi4Er6ccwnH9js0u0Y%3D"},
    {"id": 3842, "title": "一叶障目",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/114539/T5WrE7cQ.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=paSlH9YyNLj2Z1TpNVGinIKtV7o%3D"},
    {"id": 3841, "title": "一五一十",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/114519/6JwukScy.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=6rytDUcYKtCtD7Dk9ynoIMCNqn0%3D"},
    {"id": 3840, "title": "一塌糊涂",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/114459/Ay4oFCbu.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=fjyU2zUwXFVFdXMY9YVL%2BIFCjLg%3D"},
    {"id": 3839, "title": "一手遮天",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/114436/9ARTID5t.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=uDq3sIQ3QTpZjv0CvxC9G3KfKBA%3D"},
    {"id": 3838, "title": "一目十行",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/114415/axfaMRHO.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=001DwRCzJ1iNnHgxR3n8BatbpRc%3D"},
    {"id": 3837, "title": "一波三折",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/114352/mt9JvT4y.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=YLM8fDODhucaoovpJtO7SJMg8%2BU%3D"},
    {"id": 3836, "title": "扬眉吐气",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/114327/wL0qH9Sq.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=mumN7chsMh0tN1OA5o8uhOM8rLY%3D"},
    {"id": 3835, "title": "雪上加霜",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/114301/VSmYRc4Y.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=DO%2F4co7HPeUv59XERV8FoEDeCQg%3D"},
    {"id": 3834, "title": "一清二白",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/114236/QjINKv83.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=XBTl0nXuyYSL6z0fFnzhLC9TgQ4%3D"},
    {"id": 3833, "title": "悬崖勒马",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/114215/YI8n1XfM.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=VRalFpzwtdnMaduBVrgxTlkWH0s%3D"},
    {"id": 3832, "title": "心直口快",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/114156/fvb1JgMN.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=Hq8pxLsqZ6sMAXOL1xGa7qDBIqs%3D"},
    {"id": 3831, "title": "小鸟依人",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/114129/pCsqVnHm.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=ShX69PujF4E%2FNRPSJB7%2FU6bxOfQ%3D"},
    {"id": 3830, "title": "五体投地",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/114108/csLL6uwe.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=0FbE2vfqmeKnrfEmdS%2BUnEEmNxc%3D"},
    {"id": 3829, "title": "无与伦比",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/114030/ah2JTdWL.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=cjsdVxKObCgJMfMTyakgnv1UkLU%3D"},
    {"id": 3828, "title": "万里挑一",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/114007/GWMBgiHn.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=IDsDJEzBBD%2BrWOwcw%2FEk%2FSfOeXs%3D"},
    {"id": 3827, "title": "脱口而出",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/113944/ltK8tT3N.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=r9seByi4Y%2FfcthxtZiHwrPpsI9g%3D"},
    {"id": 3826, "title": "同床异梦",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/113923/g68hfikc.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=ORuT8J320Xx3FEOy0qGiP8Al2pw%3D"},
    {"id": 3825, "title": "天方夜谭",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/113851/a6S4YTYa.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=VDi9zBIjbiyq9U%2FPBTWnHgS3N9Y%3D"},
    {"id": 3824, "title": "四脚朝天",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/113830/6vLL80DK.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=jzBYwJn3ZTKORgL9ukw7iA6tDyM%3D"},
    {"id": 3823, "title": "四大皆空",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/113808/yFsdOzFE.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=c5vM%2BcY6O4UM2s6cmSG20U%2BF2Lk%3D"},
    {"id": 3822, "title": "顺手牵羊",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/113746/bFiSwYMZ.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=rHO%2BK8fs3kfFIMUTXJEjH4niTmg%3D"},
    {"id": 3821, "title": "水到渠成",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/113709/4Wt4r8Ea.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=%2B9Xzw6PYxdVnc6AlmlK3t%2FCslKA%3D"},
    {"id": 3820, "title": "事半功倍",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/113648/MJTpZpNA.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=Tju9ENPsiNKjQ7NLQdl0fg7RxRE%3D"},
    {"id": 3819, "title": "石破天惊",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/113621/cCV89VwT.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=Q9gI2q%2FJLluWjmGP5dbYjZs7o%2BA%3D"},
    {"id": 3818, "title": "声东击西",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/113553/ucMl58v0.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=3sKrzbYZp%2Fl1unThkXSJq7CUUBI%3D"},
    {"id": 3817, "title": "三长两短",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/113532/Be4AJ01x.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=vJm2kMxQK8H4KrMO5n2%2BTbeTSG8%3D"},
    {"id": 3816, "title": "三言两语",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/113512/KfziwLvL.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=4fxJzrYcpVv9MgCnsBYJzo8uNHw%3D"},
    {"id": 3815, "title": "三六九等",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/113449/4L3bjUfi.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=RUXBtaSSSVVRoL0TaJ14VnC0kmc%3D"},
    {"id": 3814, "title": "弱不禁风",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/113416/jTfJx7Er.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=7PBurVM3bWNyYDfsH9ZaeOQ7pvY%3D"},
    {"id": 3813, "title": "深不可测",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/113354/6Ly1yfC2.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=eLjMTwEE%2BrBu9kuCmOQkNdlTgOo%3D"},
    {"id": 3812, "title": "入木三分",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/113323/zzOf6Nb1.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=YHrlhbdQDT3v02%2BciVcYCPF2sCE%3D"},
    {"id": 3811, "title": "如坐针毡",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/113301/OUeAsqZk.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=JeNBy6U2WpbVO4m0yXfgHq%2F%2FWNM%3D"},
    {"id": 3810, "title": "穷山恶水",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/113239/ZxG3IfeS.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=SkEB%2BFib%2FpVcRQ7oiYQdH8l%2BIpM%3D"},
    {"id": 3809, "title": "倾国倾城",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/113218/WnzK6rSW.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=DerNmk%2B0kjR91VwXZtBUA5P74ec%3D"},
    {"id": 3808, "title": "气吞山河",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/113155/3lbATxUM.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=UstjBZvqZxq0jPgd6stjnoUHmto%3D"},
    {"id": 3807, "title": "骑虎难下",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/113130/aJrey8zz.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=xdn00EAnGQPVfcOVKB9%2B4gKiggY%3D"},
    {"id": 3806, "title": "明枪暗箭",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/112706/tROGweBy.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=2cBDItH53H1fYLen6N4%2F6XfPQ9s%3D"},
    {"id": 3805, "title": "貌合神离",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/112638/uCKRiwRX.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=SZgGLWwbHGlbUAWzaugQkYsDzYQ%3D"},
    {"id": 3804, "title": "马失前蹄",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/112551/EV7x65MI.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=OuQdEay1bRLtPTtp7V85CD2oetg%3D"},
    {"id": 3803, "title": "柳暗花明",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/112521/zAzxhQmD.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=N5Iactu6rQfPBf8i9CiwX%2FnERRc%3D"},
    {"id": 3802, "title": "历历在目",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/112455/oVINeIDu.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=ccfHXCvAsJY80gZ5cRIU4caRw8A%3D"},
    {"id": 3801, "title": "里应外合",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/112329/LyuUQKly.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=fvSjdJLxZYEPvTtP7H57ll9Mglg%3D"},
    {"id": 3800, "title": "夸父逐日",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/112258/cSrn4Dce.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=cVu6ID2KZg87y7m02hizux5E%2FCo%3D"},
    {"id": 3799, "title": "苦中作乐",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/112227/Fm8u5R8b.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=CdyukXQSXC4QqAfk8WCwaC3szyk%3D"},
    {"id": 3798, "title": "口是心非",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/112116/L6aZQzyR.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=dlcTFUpTQaBT9CHXd8znZmKyUN4%3D"},
    {"id": 3797, "title": "可圈可点",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/111931/zBMNzOrT.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=WdGYNjehJNy35vMps%2FBTOJA66Pg%3D"},
    {"id": 3796, "title": "开门见山",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/111905/ZK0j0QrW.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=PABrc94q0C6Hrs1tSoh7nGa58go%3D"},
    {"id": 3795, "title": "举一反三",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/111820/ZxX2oAmd.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=lm4dwVpzDR17E0Mx0IUCtrQFGoI%3D"},
    {"id": 3794, "title": "居高临下",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/111752/ujdxjhdS.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=Um6CSTY2uho4KQFPohqOiFFyzv4%3D"},
    {"id": 3793, "title": "惊弓之鸟",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/111708/VpFxNliQ.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=u0udbl8fhOatKEfNGxRGq20%2B%2B%2F8%3D"},
    {"id": 3792, "title": "锦上添花",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/111630/A3Ff8iZi.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=b%2BsE6c2f%2F2uJ2FLF2eIUtf%2F7jEY%3D"},
    {"id": 3791, "title": "见钱眼开",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/111430/fF3ZOdAO.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=eA%2BU3hkJDQo6oBRBSdeu6PB74fg%3D"},
    {"id": 3790, "title": "见缝插针",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/111337/8u5EQGhv.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=4Ti%2FetdazkxBGU3adj7PtM53EDg%3D"},
    {"id": 3789, "title": "鸡毛蒜皮",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/111252/fB4lTRPK.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=LD%2FI4%2Fr9kzqewnEtAPRuMYnfRsY%3D"},
    {"id": 3788, "title": "鸡飞蛋打",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/111217/1TcsjrBj.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=bTC2AfolV9QcrgM3GoCJH5iH7%2Bk%3D"},
    {"id": 3787, "title": "火上浇油",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/111135/HeYVWJzC.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=B7GTdItZjbzbP%2BR21E1KQZPUdAM%3D"},
    {"id": 3786, "title": "横冲直撞",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/105343/fgoX8ZSR.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=INKdbFYq4h4yy%2B7q3iTkMJTc1cE%3D"},
    {"id": 3785, "title": "狗急跳墙",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/105307/zNt9soR5.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=uwbvyieBWSTOQbvrBfY9iWRhLGs%3D"},
    {"id": 3784, "title": "隔靴搔痒",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/105235/6Krsixti.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=dxD8UDSXPhG%2BO20hpPw5kMjZRyk%3D"},
    {"id": 3783, "title": "覆水难收",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/105152/fHPfEc65.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=KeFhTaXmyC5vxkPufP3MOh%2FUTu0%3D"},
    {"id": 3782, "title": "排山倒海",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/105134/ofcyxI85.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=e%2BzIrmzi9SCmFZiOG26fe8FSCno%3D"},
    {"id": 3781, "title": "非同小可",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/105112/bvqBFqz3.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=%2Ff0ZLRh9FCvq7n42fKca8vZYQ%2B4%3D"},
    {"id": 3780, "title": "飞黄腾达",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/105037/ZsNzdbty.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=uJXm%2FjYt2nwh2i9NxPbGzQ%2BOMX8%3D"},
    {"id": 3779, "title": "多此一举",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/104846/Yv8yHEHE.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=cqag9YaCczbtBA2Upg8kyCjz25E%3D"},
    {"id": 3778, "title": "拍案叫绝",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/104825/5eB01eYj.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=vLIxIinRH7xkIohEQKEa7%2FLdgrM%3D"},
    {"id": 3777, "title": "断章取义",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/104755/hlnhj3Ls.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=LnJ4cNEj9MqhJo0zodI1eNlyiWk%3D"},
    {"id": 3776, "title": "能屈能伸",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/104721/nSEAHUHG.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=3yqDUKrgGGZ%2BhnMWdM%2F8FbCRFCU%3D"},
    {"id": 3775, "title": "独当一面",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/104702/D7jzt24E.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=Ja0wRcmAssQkimWEkjr%2BvvG7jzA%3D"},
    {"id": 3774, "title": "目不识丁",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/104649/sYkdwFti.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=yr5eS72F1EnAUXQnhX%2BiveYwBhM%3D"},
    {"id": 3773, "title": "点到即止",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/104541/Rg8KpWG0.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=%2FRXZrQd9vg61egwNnCjxhSoew%2F0%3D"},
    {"id": 3772, "title": "颠倒黑白",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/104503/Ft8favj7.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=rtA8yeRnSvFAvmfO8NjLAjFZzWs%3D"},
    {"id": 3771, "title": "德高望重",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/104421/oJFhG16V.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=CszA1NFizSPCV5%2BHY8%2FHs1Z4qng%3D"},
    {"id": 3770, "title": "胆大包天",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/104350/Fn9N2xKG.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=96VHqGnvp%2F9A0IBpgvdDz1f8gGw%3D"},
    {"id": 3769, "title": "呆若木鸡",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/104313/YSl4zZgu.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=gPu9m9nVf3YUyXxyiHVDhJPVm%2B0%3D"},
    {"id": 3768, "title": "大显身手",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/104225/McVQgeJn.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=c2n6BqhSltADiSCkNdtnzNFJ9m4%3D"},
    {"id": 3767, "title": "大惊小怪",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/104149/W4lkeORD.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=RSyf8qza5B4MniTjsSlUnxqdJL4%3D"},
    {"id": 3766, "title": "大步流星",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/104040/JJVOigc9.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=KFzHhEEdRbbSkWOVRz7CL2hNlAM%3D"},
    {"id": 3765, "title": "唇亡齿寒",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/104013/GBeyIG35.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=Jj9Ipeog7vq7frueM07Lw9P2IPY%3D"},
    {"id": 3764, "title": "朝三暮四",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/103943/wYA5RsVJ.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=NEiryY89eGjiEdOZJj%2Fm44SrBOI%3D"},
    {"id": 3763, "title": "参差不齐",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/103912/1Xby4n8U.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=fUV96qCdMee%2FfFByOgxpFXewCFA%3D"},
    {"id": 3762, "title": "比翼双飞",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/103831/uOvrYKNO.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=cpmYyNkzcHx%2BNi14c34q2Gub3Qs%3D"},
    {"id": 3761, "title": "本末倒置",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/103756/0HbO6lw8.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=nbXXqJonnoUVALmmEuZfz4SILao%3D"},
    {"id": 3760, "title": "背道而驰",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/103717/APksODPX.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=fPoAHbqA6IYaEg0Bgv6xtwzyrmI%3D"},
    {"id": 3759, "title": "杯弓蛇影",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/103625/ztdO6O6l.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=2Ft%2FAvWQzRjLvc430Ne4F3I4LJE%3D"},
    {"id": 3758, "title": "半斤八两",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/103546/3zS3qAnY.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=KgnohaPdq3IZ6DG7tIk82Mot2kY%3D"},
    {"id": 3757, "title": "半壁江山",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/103514/Na0IGQTd.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=pSvrP0c8VuLw38sKwhEmPaVhCPc%3D"},
    {"id": 3756, "title": "白纸黑字",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/103433/hLPrQfYp.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=kwMW7NtC%2FBgPDODsChH9RuuJohU%3D"},
    {"id": 3755, "title": "八仙过海",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/103350/bN7la5YS.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=hCK21Im5b7%2FsciTGik2Wm0COnLU%3D"},
    {"id": 3754, "title": "爱憎分明",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/103227/sTbshzQ5.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=CZcUpGKGYk18OMqLl5suPh5M32s%3D"},
    {"id": 3753, "title": "唉声叹气",
     "img_url": "https://s3.harix.iamidata.com/crss-smartomp-221/cms/zh-CN/20220822/103113/2hT9lbRB.png?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K&Expires=4743019496&Signature=FAaNCvABDavNH%2BoSfPQHj000f4Y%3D"}]


def get_n_topics():
    """从题库随机抽取n道题目 存入变量topics中"""
    rounds = proResult["session"]["variables"]["rounds"]["value"]
    topics = random.sample(topic_list, int(rounds))
    proResult["session"]["variables"]["topics"] = {"key": "topics", "value": json.dumps(topics, ensure_ascii=False)}


def get_one_topic():
    """从题库抽取1道题目 分别存入变量 now_question now_answer now_round 中"""
    # 从题库中随机抽取一题
    topics = proResult["session"]["variables"]["topics"]["value"]
    topic_list = json.loads(topics)
    now_topic = topic_list.pop()

    # 将题目全部信息存入 now_topic
    proResult["session"]["variables"]["now_topic"] = {"key": "now_topic",
                                                      "value": json.dumps(now_topic, ensure_ascii=False)}
    # 将剩余题目放回原处 topics
    proResult["session"]["variables"]["topics"] = {"key": "topics",
                                                   "value": json.dumps(topic_list, ensure_ascii=False)}
    # 设置当前是第几轮 now_round
    if proResult["session"]["variables"].__contains__("now_round"):
        now_round = int(proResult["session"]["variables"]["now_round"]["value"]) + 1
    else:
        now_round = 1
    proResult["session"]["variables"]["now_round"] = {"key": "now_round", "value": str(now_round)}

    # 将向用户投放题目存入变量 now_question now_answer
    now_question = now_topic["img_url"]
    now_answer = now_topic["title"]
    proResult["session"]["variables"]["now_question"] = {"key": "now_question", "value": now_question}
    proResult["session"]["variables"]["now_answer"] = {"key": "now_answer", "value": now_answer}


def summary_for_topic():
    """答题结束 统计答题正确数 返回回复话术"""
    if proResult["session"]["variables"].__contains__("right_count"):  # 若一次都没回答正确 就不会产生变量right_count
        right_count = proResult["session"]["variables"]["right_count"]["value"]
    else:
        right_count = 0

    rounds = proResult["session"]["variables"]["rounds"]["value"]
    if int(right_count) >= int(0.6 * int(rounds)):
        answer_final = "success"
    else:
        answer_final = "fail"

    proResult["session"]["variables"]["game_over_reply"] = {"key": "game_over_reply", "value": answer_final}
    proResult["session"]["variables"]["wrong_count"] = {"key": "wrong_count", "value": str(int(rounds)-int(right_count))}
