from linebot import LineBotApi

from linebot.models import (
    TextSendMessage, ImageSendMessage, TemplateSendMessage, ButtonsTemplate, PostbackAction, MessageAction, URIAction,
    CarouselTemplate, CarouselColumn, LocationSendMessage, AudioSendMessage, StickerSendMessage, VideoSendMessage)
from linebot.exceptions import LineBotApiError

class Demo(object):

    def __init__(self):
        self.CHANNEL_ACCESS_TOKEN = "xwYcIrRNGmj7SKJGpl2DSe+GdJ6JEFQXdoBTaVGLkNGPVdTrSTBKeDDxH3CJzK2eTfgIHHq60evtHvhWF1ldXa2h5SKXyMQKEiSVnpDQuxhzC9lwPTqYaSV88lMmGqxolbQrKgOTBMqLO2yjfM71cQdB04t89/1O/w1cDnyilFU="
        self.to = "U2fce467c4cae2847a7d19d631a387782"
        self.line_bot_api = LineBotApi(self.CHANNEL_ACCESS_TOKEN)

    def video_msg(self):
        video_message = VideoSendMessage(
            original_content_url='https://drive.google.com/uc?export=download&id=11OZi2D2fafF3cLVojMVdYUT-Ug2fYPLx',
            preview_image_url='https://drive.google.com/uc?export=download&id=1wsz3U2Aqk4oR83UsvA-EH9J5ffcShsvA'
        )

        try:
            self.line_bot_api.push_message(self.to, video_message)
        except LineBotApiError as e:
            # error handle
            raise e   