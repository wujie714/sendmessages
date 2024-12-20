# sendmessags
The Plugin of dify-on-wechat
#配置
##修改 dify-on-wechat的plugin目录下的 plugins.json，加入：sendmessages 插件,优先级 设置 在 Godcmd 之后
'''
{
    "plugins": {
        "tool": {
            "enabled": false,
            "priority": 1901
        },
        "send_msg": {
            "enabled": true,
            "priority": 1800
        },
        "custom_dify_app": {
            "enabled": true,
            "priority": 1800
        },
        "Godcmd": {
            "enabled": true,
            "priority": 999
        },
        "sendmessages": {
            "enabled": true,
            "priority": 998
        },
        "Keyword": {
            "enabled": true,
            "priority": 900
        },
        "Banwords": {
            "enabled": false,
            "priority": 100
        },
        "linkai": {
            "enabled": false,
            "priority": 99
        },
        "JinaSum": {
            "enabled": false,
            "priority": 10
        },
        "Apilot": {
            "enabled": true,
            "priority": 9
        },
        "timetask": {
            "enabled": false,
            "priority": 8
        },
        "Hello": {
            "enabled": true,
            "priority": 1
        },
        "Role": {
            "enabled": true,
            "priority": 0
        },
        "GroupAtAutoreply": {
            "enabled": true,
            "priority": 0
        },
        "Dungeon": {
            "enabled": true,
            "priority": 0
        },
        "CustomDifyApp": {
            "enabled": true,
            "priority": 0
        },
        "BDunit": {
            "enabled": false,
            "priority": 0
        },
        "Finish": {
            "enabled": true,
            "priority": -999
        }
    }
}
'''
### 修改 config.json
{
  "mygis_stop_reply": true,  //默认情况是否回复
  "mygis_sleep_minsecond": 0, //批量群发数据时 时间最小间隔
  "mygis_sleep_maxsecond": 1, //批量群发数据时 时间最大间隔

  "mygis_friends_whitelist": ["opengis文强"],  //朋友白名单
  "mygis_groups_whitelist": ["opengis社区"], //群白名单
  "single_chat_noreply_prefix": ["收到", "好的","再见","是的","ok","OK","1"], //单聊不回复关键字
  "accept_friend_commands": ["加好友","我是","boss","求职","应聘","java","python","人工智能","数据处理"], //接受朋友关键字
  "accept_friend_msg": "很高兴认识您",//接受朋友的回复
  "response": {
    "公司资料、公司介绍、公司简介":"./plugins/sendmessages/docs/file/mygis.pdf",
    "公司网站":"http://www.mapyeah.com/",
    "公司公众号": "./plugins/sendmessages/docs/file/qrcode_for_mygis.jpg",
    "打赏": "./plugins/sendmessages/docs/file/pay.jpg",
    "入群、进群": "opengis社区"
  },
  "instrution":{
      "公司资料": ["./plugins/sendmessages/docs/file/mygis.pdf","./plugins/sendmessages/docs/file/mygis.pdf"],// 相对于 dify-on-wechat的根目录,支持:http/https
      "公司公众号":["九鼎图业 公众号，请关注","./plugins/sendmessages/docs/file/qrcode_for_mygis.jpg"],
      "opengis公众号":["新推出 opengis 公众号，请关注","./plugins/sendmessages/docs/file/qrcode_for_opengis.jpg"]     //逐条发送
   }
}

##使用 帮助
$sendmessages
