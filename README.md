# QQLightInterface4Python
## 给QQLight写的python接口

# 受上游影响，Mahua框架已于2020年8月2日封存[（链接）](https://www.newbe.pro/Newbe.Mahua/Newbe-Mahua.Archive/#more)，本项目已失去存在意义

### 简介 Introduction
自己在用QQLight机器人的时候, 调用[Mahua](http://www.newbe.pro/2019/01/25/Newbe.Mahua/Start-With-Mahua-In-V2.0/)的HTTP接口, 
每次都要自己写一长串形如以下的代码, 就很是不爽, 于是决定自己封装一个函数用.  
```python
import urllib3
import json

url = "http://localhost:36524/api/v1/QQLight/Api_SendMsg"
data = {
    "类型": 1,
    "群组": "",
    "qQ号": "xxxxx",
    "内容": 'xxxx'
}
http = urllib3.PoolManager()
res = http.request('POST',
                     url,
                     body=json.dumps(data).encode('utf8'),
                     headers={"Content-Type": "application/json"}
                     )
```

有了这个接口, 发送qq消息只需要如下即可.  
```python
from utils import *

qq = 'xxxxx'
msg = 'xxxxx'
send_private_msg(qq, msg)
```
不仅如此, 还写了一个`QbotMessage`类, 发送文本, 图片等混合消息就不需要自己手动拼接了, 比如:
```python
from utils import *

qq = 'xxxxx'
text = 'xxxxxx'
img_path = '***path/url***'

msg = QbotMessage()
msg.add_text(text)
msg.add_img(img_path)

send_private_msg(qq, msg)
```

另外, `example`里写了一个`timed_send.TimedSendMsg`类, 用于定时发送消息,
并用其写了几个个小例子:
1. `give_me_kaguya_example`  
用QQ机器人定时发送~~辉夜大小姐的图片~~消息
   + 这个例子中的部分(pixiv相关的部分)功能依赖 `PIL` 和 [`pixivpy`](https://github.com/upbit/pixivpy)
2. `where_is_my_notice`  
定时检查学院官网的新闻, 有新的就发QQ消息提示

### 依赖 Dependencies
+ [QQLight](https://www.52chat.cc)
+ [Newbee.Mahua](http://www.newbe.pro/2019/01/25/Newbe.Mahua/Start-With-Mahua-In-V2.0/)
+ python-requests

### 用法 Usage
1. 把`utils.py`和`CONFIG.py`放在合适的位置
2. 使用
```python
from utils import *

qq = '目标qq号'

qbmsg = QbotMessage()
qbmsg.add_text("这是前面一段 hi~")
qbmsg.add_img("http://www.baidu.com/img/bd_logo1.png")
qbmsg.add_text("这是后面一段")

send_private_msg(qq, qbmsg)
```

### 进度
+ 已实现:
   + 发送各种消息(私聊, 群聊等), 支持文字和图片混排
   + ...

+ TODO
   + 发送链接卡片
   + 发送音乐卡片
   + ...
   
# 待续... 
# To be continued...
