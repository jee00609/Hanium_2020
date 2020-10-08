#-*- coding:utf-8 -*-
# 2020-10-09 제대로 실행 안됨. 문의 넣음
import urllib3
import json
import base64

openApiURL = "http://aiopen.etri.re.kr:8000/WiseASR/Pronunciation"
accessKey = "ff3e7deb-1ccf-4ee3-bc0b-292c1ef5bfd5"
audioFilePath = "audio/PRO_M_20csg0029.mp3"
languageCode = "english"
script = "PRONUNCIATION_SCRIPT"
 
file = open(audioFilePath, "rb")
audioContents = base64.b64encode(file.read()).decode("utf8")
file.close()
 
requestJson = {
    "access_key": accessKey,
    "argument": {
        "language_code": languageCode,
        "script": script,
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
 
print("[responseCode] " + str(response.status))
print("[responBody]")
print(str(response.data,"utf-8"))
