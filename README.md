# 简陋的iOS测试包分发工具
- 支持蒲公英平台
### 使用
⚠️ 不能用模拟器编译

编辑配置文件
```shell
-> ~: vi .dabao_config.yml
```
```yaml
# conf.yml
pgy:
 api_key: svew32232 #蒲公英apikey
 user_key: w232 #蒲公英userkey
weChart:
 web_hook: https://xxxxx #企业微信机器人地址
dingTalk:
 web_hook: https://xxxxx #钉钉机器人地址
email:
  - xxx@163.com #邮箱
```
打包上传
```shell
-> ~: pgydb --name project 
```
通知测试
```shell
-> ~: pgydb --send weixin
-> ~: pgydb --send dingTalk
-> ~: pgydb --send email
```