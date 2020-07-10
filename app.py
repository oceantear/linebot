from flask import Flask, request, abort
import requests
import json

from bs4 import BeautifulSoup

from linebot import (
    LineBotApi, WebhookHandler
)

from linebot.exceptions import (
    InvalidSignatureError
)

from linebot.models import (
    TextSendMessage, ImageSendMessage, TemplateSendMessage, ButtonsTemplate, PostbackAction, MessageAction, URIAction,
    CarouselTemplate, CarouselColumn, MessageEvent, TextMessage, TextSendMessage, LocationSendMessage, StickerSendMessage,
    AudioSendMessage)

app=Flask(__name__)
#Channel access token
line_bot_api = LineBotApi('xwYcIrRNGmj7SKJGpl2DSe+GdJ6JEFQXdoBTaVGLkNGPVdTrSTBKeDDxH3CJzK2eTfgIHHq60evtHvhWF1ldXa2h5SKXyMQKEiSVnpDQuxhzC9lwPTqYaSV88lMmGqxolbQrKgOTBMqLO2yjfM71cQdB04t89/1O/w1cDnyilFU=')
#channel secret
handler = WebhookHandler('c07bdeb9cdabc6c14307c208d5dd7ba0')

@app.route('/')
def hello():
    return 'hello !'

@app.route('/test')
def test():
    return "test"

@app.route('/callback', methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    print("body: ", body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

def oil_price():
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
    #print("oil_price:")
    #print(content)
    return content

def stock_price():
    try:
        content = get_stock_price(stockID)
        content = '{}\n{}\n{}\n'.format('股票代號 : ' + content['股票代號'],'公司簡稱 : ' + content['公司簡稱'], '當盤成交價 : ' + content['當盤成交價'])
        print('content :')
        print(content)
        line_bot_api.push_message(to, TextSendMessage(text=content))
    except InvalidSignatureError:
        abort(400)
    return 'OK'

def get_stock_price(id):
    target_url = 'https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_'+ id + '.tw'

    rs = requests.session()
    res = rs.get(target_url, verify=False)
    msgArray = json.loads(res.text)
    data = msgArray['msgArray'][0]
    print('data :')
    print(data)
    print(data['c'])
    meta = { '股票代號': data['c'],
                '公司簡稱':data['n'],
                '當盤成交價':data['z'],
                '當盤成交量':data['tv'],
                '累積成交量':data['v'],
                '開盤價':data['o'],
                '最高價':data['h'],
                '最低價':data['l'],
                '昨收價':data['y'],
        }
    
    return meta 


def ptt_beauty():
    print("ptt_beauty")
    rs = requests.session()
    res = rs.get('https://www.ptt.cc/bbs/Beauty/index.html', verify=False, cookies={'over18':'1'})
    
    soup = BeautifulSoup(res.text, 'html.parser')
    all_page_url = soup.select("div.r-ent")
    info = list()
    meta = dict()
    
    for entry in all_page_url:
        #print("推:")
        #print(entry.find('a').text)
        if entry.find('a') is not None:
            if("公告" not in entry.find('a').text):
                meta = { 'title': entry.find('a').text,
                        'link': entry.find('a').attrs['href'],
                        'author':entry.find('div', 'meta').find('div','author').text,
                        'push':entry.find('div','nrec').text,
                        'Imgurl':""
                        
                }
        
        if meta is not None:
            
            rate = meta.get("push")

            if rate :
                rate = 100 if rate.startswith('爆') else rate
                rate = -1 * int(rate[1]) if rate.startswith('X') else rate
            else:
                rate = 0    

            if int(rate) >= 20:
                print('rate > 20')
                print('https://www.ptt.cc/'+ meta.get('link'))
                
                title = meta.get("title")
                print('title : '+ meta.get('title'))
                res = rs.get('https://www.ptt.cc/'+ meta.get('link'), verify=False, cookies={'over18':'1'})
                #print("sub")
                #print(res.text)
                soup = BeautifulSoup(res.text, 'html.parser')
                #des = soup.find('meta', attrs={'name': 'description'})
                try:
                    for img in soup.find_all("a", rel='nofollow'):
                        img_url = image_url(img['href'])
                        if img_url is not None:
                            meta['Imgurl'] = img_url
                            info.append(meta)
                            print("img_url : ")
                            print(img_url)
                            break
                except Exception as e:
                    print("自行刪除標題列", e)

    print("final meta : ")
    print(info) 
    return info               

def image_url(link):
        # 不抓相簿 和 .gif
        if ('imgur.com/a/' in link) or ('imgur.com/gallery/' in link) or ('.gif' in link):
            return []
        # 符合圖片格式的網址
        images_format = ['.jpg', '.png', '.jpeg']
        for image in images_format:
            if link.endswith(image):
                return link
        # 有些網址會沒有檔案格式， "https://imgur.com/xxx"
        if 'imgur' in link:
            return ['{}.jpg'.format(link)]
        return None                 

def gen_Carousel_template_msg(info):

    msg = list()
    for data in info:
        print("title :", data.get('title'))
        print("link :", "https://www.ptt.cc" + data.get('link'))
        print("Imgurl :", data.get('Imgurl'))
        url = "http://www.ptt.cc" + data.get('link')
        msg.append(CarouselColumn(
                        thumbnail_image_url= data.get('Imgurl'),
                        title=data.get('title'),
                        text=data.get('author'),
                        actions=[
                            URIAction(
                                label='點擊看正妹',
                                uri=url
                            )
                        ]
                    ))
    return msg                   

def location_msg(event):
    location_message = LocationSendMessage(
        title='我的位置',
        address='資拓宏宇',
        latitude=25.0144456,
        longitude=121.4610858
    )
    
    line_bot_api.reply_message(event.reply_token, location_message)

def audio_msg(event):
    audio_message = AudioSendMessage(
        original_content_url='https://example.com/original.m4a',
        duration=240000
    )
    line_bot_api.reply_message(event.reply_token, audio_message)

def stick_msg(event):
    sticker_message = StickerSendMessage(
        package_id='1',
        sticker_id='1'
    )
    line_bot_api.reply_message(event.reply_token, sticker_message)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("event.reply_token:", event.reply_token)
    print("event.message.text:", event.message.text)
    #msg = msg.encode('utf-8')

    if "表特" in event.message.text or "beauty" in event.message.text:
        content = ptt_beauty()
        msg = gen_Carousel_template_msg(content)
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(alt_text='ptt 表特',
            template=CarouselTemplate(
                columns= msg
            )))
    
        return 0
    elif event.message.text == "油價":
        content = oil_price()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    elif "股價" in event.message.text:
        stockID = event.message.text.split("股價")
        print('stockID :'+stockID[0])
        content = get_stock_price(stockID[0])
        content = '{}\n{}\n{}\n'.format('股票代號 : ' + content['股票代號'],'公司簡稱 : ' + content['公司簡稱'], '當盤成交價 : ' + content['當盤成交價'])
        print('content :')
        print(content)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
    elif "教學" in event.message.text or "help" in event.message.text:
        content = '{}\n{}\n{}\n'.format('表特 指令: 表特/beauty','油價 指令: 油價', '股價 指令:  2330股價')
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
    elif "Demo" in event.message.text.lower():
        input = event.message.text.split("Demo")
        command = input[1]
        print('command :', command)
        if "address" in command:
            location_msg(event)
        elif "audio" in command:
            audio_msg(event)
        elif "stick" in command:
            stick_msg(event)              
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="我還沒學會這項功能，敬請期待~"))
        return 0    

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,debug=True)