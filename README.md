# QQLightInterface4Python
## 给QQLight写的python接口

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
from util import *

qq = 'xxxxx'
msg = 'xxxxx'
send_message(qq, 'private', msg)
```
不仅如此, 还写了一个`QbotMessage`类, 发送文本, 图片等混合消息就不需要自己手动拼接了, 比如:
```python
from util import *

qq = 'xxxxx'
text = 'xxxxxx'
img_path = '***path/url***'

msg = QbotMessage()
msg.add_text(text)
msg.add_img(img_path)
msg = msg.boil()

send_message(qq, 'private', msg)
```

另外, `example`里写了两个小例子, 分别是
1. `give_me_kaguya`  
用QQ机器人定时发送~~辉夜大小姐的图片~~消息
2. `where_is_my_notice`  
定时检查学院官网的新闻, 有新的就发QQ消息提示

### 依赖 Dependencies
+ QQLight
+ Mahua.Framework
+ python-requests

### 用法 Usage
1. 安装 [QQLight](https://www.52chat.cc)
2. 安装 [Newbee.Mahua](http://www.newbe.pro/2019/01/25/Newbe.Mahua/Start-With-Mahua-In-V2.0/)
3. 把`util.py`和`CONFIG.py`放在合适的位置
4. 使用
```python
from util import *

qq = '目标qq号'

qbmsg = QbotMessage()
qbmsg.add_text("这是前面一段 hi~")
qbmsg.add_img("http://www.baidu.com/img/bd_logo1.png")
qbmsg.add_text("这是后面一段")

send_private_msg(qq, qbmsg)
```

### 进度
+ 已实现:
   + 发送消息, 支持文字和图片混排
   + ...

+ TODO
   + 发送链接卡片
   + 发送音乐卡片
   + ...
   
# 待续... 
# To be continued...
