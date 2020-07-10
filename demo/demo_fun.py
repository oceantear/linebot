from linebot import LineBotApi

from linebot.models import (
    TextSendMessage, ImageSendMessage, TemplateSendMessage, ButtonsTemplate, PostbackAction, MessageAction, URIAction,
    CarouselTemplate, CarouselColumn, LocationSendMessage, AudioSendMessage, StickerSendMessage, VideoSendMessage)
from linebot.exceptions import LineBotApiError

class Video_demo(object):

    def __init__(self, event):
        self.CHANNEL_ACCESS_TOKEN = "xwYcIrRNGmj7SKJGpl2DSe+GdJ6JEFQXdoBTaVGLkNGPVdTrSTBKeDDxH3CJzK2eTfgIHHq60evtHvhWF1ldXa2h5SKXyMQKEiSVnpDQuxhzC9lwPTqYaSV88lMmGqxolbQrKgOTBMqLO2yjfM71cQdB04t89/1O/w1cDnyilFU="
        self.to = "U2fce467c4cae2847a7d19d631a387782"
        self.line_bot_api = LineBotApi(self.CHANNEL_ACCESS_TOKEN)
        self.event = event

    def push_video_msg(self):
        video_message = VideoSendMessage(
            original_content_url='https://drive.google.com/uc?export=download&id=11OZi2D2fafF3cLVojMVdYUT-Ug2fYPLx',
            preview_image_url='https://drive.google.com/uc?export=download&id=1wsz3U2Aqk4oR83UsvA-EH9J5ffcShsvA'
        )

        try:
            self.line_bot_api.push_message(self.to, video_message)
        except LineBotApiError as e:
            # error handle
            raise e

    def img_msg(self):
        image_url = "https://i.guim.co.uk/img/media/22bed68981e92d7a9ff204ed7d7f5776a16468fe/1933_1513_3623_2173/master/3623.jpg?width=605&quality=45&auto=format&fit=max&dpr=2&s=da5b088be9a2aa1527f7509ce6a70c68"    
        img_message = ImageSendMessage(
            original_content_url=image_url, 
            preview_image_url=image_url)

        self.line_bot_api.reply_message(self.event.reply_token, img_message)    
                       

    def location_msg(event):
        location_message = LocationSendMessage(
            title='我的位置',
            address='資拓宏宇',
            latitude=25.0144456,
            longitude=121.4610858
        )
        
        self.line_bot_api.reply_message(event.reply_token, location_message)

    def audio_msg(event):
        audio_message = AudioSendMessage(
            original_content_url='https://drive.google.com/uc?export=download&id=1c3O7Ab44noGO0bXGTGzDJlR1W70Czvih',
            duration=240000
        )
        line_bot_api.reply_message(event.reply_token, audio_message)

    def video_msg(event):
        video_message = VideoSendMessage(
            original_content_url='https://drive.google.com/uc?export=download&id=11OZi2D2fafF3cLVojMVdYUT-Ug2fYPLx',
            preview_image_url='https://drive.google.com/uc?export=download&id=1wsz3U2Aqk4oR83UsvA-EH9J5ffcShsvA'
        )

        line_bot_api.reply_message(event.reply_token, video_message)    

    def stick_msg(event):
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='1'
        )
        line_bot_api.reply_message(event.reply_token, sticker_message)         