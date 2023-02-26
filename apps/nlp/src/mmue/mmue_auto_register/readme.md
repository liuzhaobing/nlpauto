## RDP用户自动注册MMUE平台

### 注册步骤

1.创建角色

2.创建MMUE用户

3.关联绑定用户与角色

### 术语说明

角色==agent

### 文件说明

conf_env_list.json 存放MMUE平台信息

conf_user_list.json 存放待创建的用户信息

mmue_user_manage.py 用户注册脚本

### 使用指南

#### 1.添加待创建用户到 conf_user_list.json

```json
{
  "users": [
    {
      "username": "wangerxiao",
      "password": "wangerxiao"
    },
    {
      "username": "zhangsanfeng",
      "password": "zhangsanfeng"
    }
  ]
}
```

##### 参数说明

username 待创建的用户名

password 待创建的用户密码

#### 2.更新MMUE平台环境信息 conf_env_list.json

```json
{
  "env_label": "dit87",
  "mmue": {
    "dit87": {
      "base_url": "https://mmue-dit87.harix.iamidata.com",
      "username": "admin",
      "password": "xxxxxx",
      "timezone": "UTC+8",
      "longitude": "104.061",
      "latitude": "30.5444",
      "language": "zh-CN",
      "tenant_code": "CloudMinds_RDP",
      "dm_name": "standard",
      "scenetplid": "1",
      "scenecharid": "32",
      "skilltplid": "1"
    }
  }
}
```

##### 参数说明
env_label 指定mmue中的某个环境 其值与conf_env_list.json["mmue"]下的键对应

mmue MMUE平台环境信息表

base_url MMUE前端地址

username 管理员登录用户名

password 管理员登录密码

timezone [角色]时区预设

longitude latitude [角色]地理位置预设

language [角色]语言预设

tenant_code [角色]租户code预设(以实际环境为准)

dm_name [角色]DM流程预设(以实际环境为准)

scenetplid [角色]客户场景id(以实际环境为准)

scenecharid [角色]场景人设id(以实际环境为准)

skilltplid [角色]技能类型id(以实际环境为准)

#### 3.运行脚本 mmue_user_manage.py

```shell
pip3 install -r requirements.txt
python3 mmue_user_manage.py
```
