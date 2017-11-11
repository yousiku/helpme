import time


class Msg:
    def __init__(self, from_user_name, to_user_name):
        self._dict = dict()
        self._dict['FromUserName'] = from_user_name
        self._dict['ToUserName'] = to_user_name
        self._dict['CreateTime'] = int(time.time())

    @property
    def data(self):
        return "success"


class TextMsg(Msg):
    def __init__(self, from_user_name, to_user_name, content):
        Msg.__init__(self, from_user_name, to_user_name)
        self._dict['Content'] = content

    @property
    def data(self):
        xml_form = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[{Content}]]></Content>
        </xml>
        """
        return xml_form.format(**self._dict)


class MediaMsg(Msg):
    def __init__(self, from_user_name, to_user_name, media_id):
        Msg.__init__(self, from_user_name, to_user_name)
        self._dict['MediaId'] = media_id

    @property
    def data(self):
        return "success"


class ImageMsg(MediaMsg):
    def __init__(self, from_user_name, to_user_name, media_id):
        MediaMsg.__init__(self, from_user_name, to_user_name, media_id)

    @property
    def data(self):
        xml_form = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[image]]></MsgType>
        <Image>
        <MediaId><![CDATA[{MediaId}]]></MediaId>
        </Image>
        </xml>
        """
        return xml_form.format(**self._dict)


class VoiceMsg(MediaMsg):
    def __init__(self, from_user_name, to_user_name, media_id):
        MediaMsg.__init__(self, from_user_name, to_user_name, media_id)

    @property
    def data(self):
        xml_form = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[voice]]></MsgType>
        <Voice>
        <MediaId><![CDATA[{MediaId}]]></MediaId>
        </Voice>
        </xml>
        """
        return xml_form.format(**self._dict)


class VideoMsg(MediaMsg):
    def __init__(self, from_user_name, to_user_name, media_id, title='自救视频', description='自救用的视频'):
        MediaMsg.__init__(self, from_user_name, to_user_name, media_id)
        self._dict['Title'] = title
        self._dict['Description'] = description

    @property
    def data(self):
        xml_form = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[video]]></MsgType>
        <Video>
        <MediaId><![CDATA[{MediaId}]]></MediaId>
        <Title><![CDATA[title]]></Title>
        <Description><![CDATA[description]]></Description>
        </Video> 
        </xml>
        """
        return xml_form.format(**self._dict)