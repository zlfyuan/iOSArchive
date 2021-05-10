# 简陋的iOS测试包分发工具
- 支持蒲公英平台
### 使用
⚠️ 不能用模拟器编译

 手动编辑配置文件 
在用户目录生成配置文件
```shell
-> ~: vi .dabao_config.ini
```
```ini
[pgySection] 
api_key = xxx
user_key = xxx

[TargetSection] 
wechat_hook = xxx
```
打包上传
```shell
-> ~: i_archive -db project 
```
通知测试
```shell
-> ~: i_archive -sd weixin
-> ~: i_archive -sd dingTalk
-> ~: i_archive -sd email
```