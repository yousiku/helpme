import requests

resp = requests.get("https://api.weixin.qq.com/cgi-bin/token", params={"grant_type": "client_credential", "appid": "wxc73ecfdc4c30d490", "secret": "a7c5a1ac1c15228fa50de257326a26a8"})
print(resp.content)
