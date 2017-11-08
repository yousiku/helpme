from flask import Flask, request
import hashlib, traceback
import xml.etree.ElementTree as ET
import time


app = Flask(__name__)


def verify_source(request):
    """
    验证请求对来源是否是微信
    :param request: flask.request
    :return: 验证正确返回echostr，否则返回空
    """
    data = request.args
    if "signature" in data and "timestamp" in data and "nonce" in data and "echostr" in data:
        signature = data["signature"]
        timestamp = data["timestamp"]
        nonce = data["nonce"]
        echostr = data["echostr"]
        token = "yousiku"
        l = [token, timestamp, nonce]
        l.sort()
        sha1 = hashlib.sha1()
        for i in l:
            sha1.update(i.encode())
        hashcode = sha1.hexdigest()
        print("handle/GET func: hashcode, signature:", hashcode, signature)
        if hashcode == signature:
            return echostr
        else:
            return ""
    else:
        return ""


@app.route('/', methods=["GET", "POST"])
def hello_world():
    try:
        if request.method == "GET":
            return verify_source(request)

        elif request.method == "POST":
            xml_data = request.data
            print(xml_data)
            data = ET.fromstring(xml_data.decode())
            server_user_name = data.find("ToUserName")
            msg_id = data.find("MsgId")
            msg_type = data.find("MsgType")
            user_name = data.find("FromUserName")
            content = data.find("Content")
            print("receive>> user: {}, msg type: {}".format(user_name.text, msg_type.text))
            if msg_type.text == "text":
                resp = ET.parse("./reply_common.xml")
            elif msg_type.text == "event":
                event = data.find("Event")
                if event.text == "subscribe":
                    resp = ET.parse("./reply_subscribe.xml")
                else:
                    return ""
            else:
                return ""
            root = resp.getroot()
            root.find("ToUserName").text = user_name.text
            root.find("FromUserName").text = server_user_name.text
            root.find("CreateTime").text = str(int(time.time()))
            r_str = ET.tostring(root, encoding="utf-8")
            print(r_str)
            return r_str
        else:
            print(request.method, request.form)
    except Exception as e:
        print(traceback.format_exc())
        return e



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
