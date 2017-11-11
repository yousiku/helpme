import xml.etree.ElementTree as ET


def parse_xml(web_data):
    """
    根据收到的数据中的消息类型实例化数据
    :param web_data: 微信消息
    :return: Msg
    """
    if len(web_data) == 0:
        return None
    xml_data = ET.fromstring(web_data)
    msg_type = xml_data.find('MsgType').text
    if msg_type == 'text':
        return TextMsg(xml_data)
    elif msg_type == 'image':
        return ImageMsg(xml_data)
    else:
        print("Unknown Msg Type: {}".format(msg_type))
        return None


class Msg:
    def __init__(self, xml_data):
        self.to_user_name = xml_data.find('ToUserName').text
        self.from_user_name = xml_data.find('FromUserName').text
        self.create_time = xml_data.find('CreateTime').text
        self.msg_type = xml_data.find('MsgType').text
        self.msg_id = xml_data.find('MsgId').text


class TextMsg(Msg):
    """
    文字消息
    """
    def __init__(self, xml_data):
        Msg.__init__(self, xml_data)
        self.content = xml_data.find('Content').text


class ImageMsg(Msg):
    """
    图片消息
    """
    def __init__(self, xml_data):
        Msg.__init__(self, xml_data)
        self.picture_url = xml_data.find('PicUrl').text
        self.media_id = xml_data.find('MediaId').text


class SubscribeMsg(Msg):
    def __init__(self, xml_data):
        Msg.__init__(self, xml_data)
        self.event = xml_data.find('Event').text
