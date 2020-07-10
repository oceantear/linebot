from linebot import LineBotApi

from linebot.models import (
    TextSendMessage, ImageSendMessage, TemplateSendMessage, ButtonsTemplate, PostbackAction, MessageAction, URIAction,
    CarouselTemplate, CarouselColumn, LocationSendMessage, AudioSendMessage, StickerSendMessage, VideoSendMessage)
from linebot.exceptions import LineBotApiError

import requests
from bs4 import BeautifulSoup

from demo.demo_fun import Demo

CHANNEL_ACCESS_TOKEN = "xwYcIrRNGmj7SKJGpl2DSe+GdJ6JEFQXdoBTaVGLkNGPVdTrSTBKeDDxH3CJzK2eTfgIHHq60evtHvhWF1ldXa2h5SKXyMQKEiSVnpDQuxhzC9lwPTqYaSV88lMmGqxolbQrKgOTBMqLO2yjfM71cQdB04t89/1O/w1cDnyilFU="
to = "U2fce467c4cae2847a7d19d631a387782"

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)

#文字訊息
def text_msg():

    target_url = 'https://gas.goodlife.tw/'
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'utf-8'
    #print(res.text)
    #print(res.content)
    print(res.encoding)
    soup = BeautifulSoup(res.text, 'html.parser')
    #soup.encoding = 'utf-8'
    title = soup.select('#main')[0].text.replace('\n', '').split('(')[0]
    gas_price = soup.select('#gas-price')[0].text.replace('\n\n\n', '').replace(' ', '')
    cpc = soup.select('#cpc')[0].text.replace(' ', '')
    content = '{}\n{}{}'.format(title, gas_price, cpc)
    print("title :", title)
    print("gas_price :", gas_price)
    print("oil_price:")
    print(content)
    #line_bot_api.reply_message(
    #        event.reply_token,
    #        TextSendMessage(text=content))
    #return content         

    try:
        line_bot_api.push_message(to, TextSendMessage(text=content))
    except LineBotApiError as e:
        # error handle
        raise e

def img_msg():
    #圖片訊息
    # ImageSendMessage物件中的輸入
    # original_content_url 以及 preview_image_url都要寫才不會報錯。
    #輸入的網址要是一個圖片，應該說只能是一個圖片，不然不會報錯但是傳過去是灰色不能用的圖
    line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
    image_url = "https://i.guim.co.uk/img/media/22bed68981e92d7a9ff204ed7d7f5776a16468fe/1933_1513_3623_2173/master/3623.jpg?width=605&quality=45&auto=format&fit=max&dpr=2&s=da5b088be9a2aa1527f7509ce6a70c68"
    try:
        line_bot_api.push_message(to, ImageSendMessage(original_content_url=image_url, preview_image_url=image_url))
    except LineBotApiError as e:
        # error handle
        raise e

def template_msg():

    line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)

    buttons_template_message = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            thumbnail_image_url='https://example.com/image.jpg',
            title='Menu',
            text='Please select',
            actions=[
                PostbackAction(
                    label='postback',
                    display_text='postback text',
                    data='action=buy&itemid=1'
                ),
                MessageAction(
                    label='message',
                    text='message text'
                ),
                URIAction(
                    label='uri',
                    uri='http://example.com/'
                )
            ]
        )
    )

    try:
        line_bot_api.push_message(to, buttons_template_message)
    except LineBotApiError as e:
        # error handle
        raise e


def Carousel_template_msg():
    CarouselColumns = list()
    CarouselColumns.append(CarouselColumn(
                    thumbnail_image_url='https://example.com/item1.jpg',
                    title='this is menu1',
                    text='description1',
                    actions=[
                        MessageAction(
                            label='message1',
                            text='message text1'
                        ),
                        URIAction(
                            label='影片介紹 阿肥bot',
                            uri='https://youtu.be/1IxtWgWxtlE'
                        ),
                        URIAction(
                            label='uri1',
                            uri='http://example.com/1'
                        )
                    ]
                ))

    CarouselColumns.append(CarouselColumn(
                    thumbnail_image_url='https://example.com/item2.jpg',
                    title='this is menu2',
                    text='description2',
                    actions=[
                        PostbackAction(
                            label='postback2',
                            display_text='postback text2',
                            data='action=buy&itemid=2'
                        ),
                        MessageAction(
                            label='message2',
                            text='message text2'
                        ),
                        URIAction(
                            label='uri2',
                            uri='http://example.com/2'
                        )
                    ]
                ))


    carousel_template_message = TemplateSendMessage(
        alt_text='Carousel template',
        template=CarouselTemplate(
            columns= CarouselColumns
        )
    )            

    try:
        line_bot_api.push_message(to, carousel_template_message)
    except LineBotApiError as e:
        # error handle
        raise e

def location_msg():
    location_message = LocationSendMessage(
        title='我的位置',
        address='資拓宏宇',
        latitude=25.0144456,
        longitude=121.4610858
    )
    try:
        line_bot_api.push_message(to, location_message)
    except LineBotApiError as e:
        # error handle
        raise e

def audio_msg():
    
    audio_message = AudioSendMessage(
        original_content_url='https://drive.google.com/uc?export=download&id=1c3O7Ab44noGO0bXGTGzDJlR1W70Czvih',
        duration=204000
    )
    try:
        line_bot_api.push_message(to, audio_message)
    except LineBotApiError as e:
        # error handle
        raise e

def stick_msg():

    sticker_message = StickerSendMessage(
        package_id='1',
        sticker_id='1'
    )

    try:
        line_bot_api.push_message(to, sticker_message)
    except LineBotApiError as e:
        # error handle
        raise e

'''def video_msg():
    video_message = VideoSendMessage(
        original_content_url='https://drive.google.com/uc?export=download&id=11OZi2D2fafF3cLVojMVdYUT-Ug2fYPLx',
        preview_image_url='https://drive.google.com/uc?export=download&id=1wsz3U2Aqk4oR83UsvA-EH9J5ffcShsvA'
    )

    try:
        line_bot_api.push_message(to, video_message)
    except LineBotApiError as e:
        # error handle
        raise e    ''' 

if __name__ == '__main__':
    demo = Demo()
    demo.video_msg()
