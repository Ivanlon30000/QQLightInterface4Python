# QQLightInterface4Python
## 给QQLight写的python接口

### 简介 Introduction
自己在用QQLight机器人的时候, 调用[Mahua](http://www.newbe.pro/2019/01/25/Newbe.Mahua/Start-With-Mahua-In-V2.0/)的HTTP接口, 
每次都要自己写一长串形如以下的代码, 就很是不爽, 于是决定自己写一个接口用.  
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

### 依赖 Dependencies
+ QQLight
+ Mahua.Framework
+ python-requests
### 用法 Usage
> 待编辑
   
      
      
# 待续... 
# To be continued...