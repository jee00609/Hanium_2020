# 2020-10-18
# mp3 파일이 아닌 raw pcm 파일로 테스트 하니 제대로 된 결과값 도출
#-*- coding:utf-8 -*-
import urllib3
import json
import base64

import urllib3
from typing import Dict

openApiURL = "http://aiopen.etri.re.kr:8000/WiseASR/Pronunciation"
accessKey = "발급받은 api"
audioFilePath = "audio/test.raw"
languageCode = "english"
script = "hello my name kim min jee"
 
file = open(audioFilePath, "rb")
audioContents = base64.b64encode(file.read()).decode("utf8")
file.close()
 
requestJson = {
    "access_key": accessKey,
    "argument": {
        "language_code": languageCode,
        "script" : script,
        "audio": audioContents
    }
}
 
http = urllib3.PoolManager()
response = http.request(
    "POST",
    openApiURL,
    headers={"Content-Type": "application/json; charset=UTF-8"},
    body=json.dumps(requestJson)
)
 
#https://minwook-shin.github.io/python-urllib3-get-url/ 참고
result = json.loads(response.data.decode('utf-8'))
print(type(result))
print(result['return_object'])

score = result['return_object']['score']
print(score)
