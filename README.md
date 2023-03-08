# TextCorrection
The text correction tools from xfyun api

## Requirement
* python3.x
* Request
* json
* configparser
## Usage
1. 首先在讯飞云网站申请一个APPID，APPKEY和APISecret，网址为https://console.xfyun.cn/services/text_check
2. 将申请的认证信息复制到本项目的config.ini文件所对应的关键字中
3. 开启终端，windows/CMD，macos/terminal等等
4. > python TextCorrection.py
5. 修改后的文本会打印到终端中，更正的地方用黄色字体"[xxx]"表示


### 使用效果
个人体验还行，准确率不高，但召回率高