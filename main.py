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
            rec_msg = receive.parse_xml(xml_data)
            if isinstance(rec_msg, receive.Msg):
                print("<<<<<", rec_msg.msg_type)
                user = rec_msg.from_user_name
                me = rec_msg.to_user_name
                if rec_msg.msg_type == "text":
                    content = "等那个脑残程序员把代码写完我再来找你。不要问我为什么，我也很无奈"
                    return reply.TextMsg(me, user, content).data
                elif rec_msg.msg_type == "image":
                    media_id = rec_msg.media_id
                    return reply.ImageMsg(me, user, media_id).data
                elif rec_msg.msg_type == 'voice':
                    media_id = rec_msg.media_id
                    return reply.VoiceMsg(me, user, media_id).data
                elif rec_msg.msg_type == 'video' or rec_msg.msg_type == 'shortvideo':
                    # FIXME 发送视频不成功，暂时先发送缩略图
                    media_id = rec_msg.media_id
                    thumb_media_id = rec_msg.thumb_media_id
                    return reply.ImageMsg(me, user, thumb_media_id).data
                elif rec_msg.msg_type == 'location':
                    content = "位置：{}, 经：{}, 纬：{}, 缩放：{}".format(
                        rec_msg.label, rec_msg.location_y, rec_msg.location_x, rec_msg.scale)
                    return reply.TextMsg(me, user, content).data
                elif rec_msg.msg_type == "event":
                    content = "哈喽，我现在还不能用哦~"
                    return reply.TextMsg(me, user, content).data
                else:
                    print("消息类型", rec_msg.msg_type, type(rec_msg.msg_type))
                    return "success"
            elif rec_msg is None:
                return "success"
            else:
                print("暂不处理", rec_msg.msg_type)
                return "success"
        else:
            print(request.method, request.form)
            return ""
    except Exception as e:
        print(traceback.format_exc())
        return e


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
