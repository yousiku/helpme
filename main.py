from flask import Flask, request
import hashlib, traceback
import receive
import reply


app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def hello_world():
    try:
        if request.method == "GET":
            data = request.args
            print(data)
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
        elif request.method == "POST":
            xml_data = request.data
            rec = receive.parse_xml(xml_data)
            if isinstance(rec, receive.Msg):
                print("<<<<<", "MSG", rec.msg_type)
                user = rec.from_user_name
                me = rec.to_user_name
                if rec.msg_type == "text":
                    content = "等那个脑残程序员把代码写完我再来找你。不要问我为什么，我也很无奈"
                    return reply.TextMsg(me, user, content).data
                elif rec.msg_type == "image":
                    media_id = rec.media_id
                    return reply.ImageMsg(me, user, media_id).data
                elif rec.msg_type == "voice":
                    media_id = rec.media_id
                    return reply.VoiceMsg(me, user, media_id).data
                elif rec.msg_type == "video" or rec.msg_type == "shortvideo":
                    # FIXME 发送视频不成功，暂时先发送缩略图
                    media_id = rec.media_id
                    thumb_media_id = rec.thumb_media_id
                    return reply.ImageMsg(me, user, thumb_media_id).data
                elif rec.msg_type == "location":
                    content = "位置：{}, 经：{}, 纬：{}, 缩放：{}".format(
                        rec.label, rec.location_y, rec.location_x, rec.scale)
                    return reply.TextMsg(me, user, content).data
                elif rec.msg_type == "link":
                    content = "标题：{}\n链接：{}\n描述：{}\n".format(rec.title, rec.url, rec.description)
                    return reply.TextMsg(me, user, content).data
                else:
                    print("未处理的消息类型", rec.msg_type)
                    return "success"
            elif isinstance(rec, receive.Event):
                print("<<<<<", "EVENT", rec.event)
                user = rec.from_user_name
                me = rec.to_user_name
                if rec.event == "subscribe":
                    content = "哈喽，我现在还不能用哦~"
                    return reply.TextMsg(me, user, content).data
                else:
                    print("未处理的事件类型", rec.event)
            elif rec is None:
                print("得到了空数据")
                return "success"
            else:
                print("暂不处理", rec.msg_type)
                return "success"
        else:
            print(request.method, request.form)
            return ""
    except Exception as e:
        print(traceback.format_exc())
        return e


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
