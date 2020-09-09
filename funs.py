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
    CarouselTemplate, CarouselColumn, MessageEvent, TextMessage, TextSendMessage)
from linebot.exceptions import LineBotApiError

from geopy.geocoders import Nominatim

app=Flask(__name__)
#Channel access token
line_bot_api = LineBotApi('xwYcIrRNGmj7SKJGpl2DSe+GdJ6JEFQXdoBTaVGLkNGPVdTrSTBKeDDxH3CJzK2eTfgIHHq60evtHvhWF1ldXa2h5SKXyMQKEiSVnpDQuxhzC9lwPTqYaSV88lMmGqxolbQrKgOTBMqLO2yjfM71cQdB04t89/1O/w1cDnyilFU=')
#channel secret
handler = WebhookHandler('c07bdeb9cdabc6c14307c208d5dd7ba0')

to = "U2fce467c4cae2847a7d19d631a387782"

@app.route('/')
def hello():
    return 'hello !'

@app.route('/test')
def test():
    return "test"

@app.route('/callback', methods=['POST','GET'])
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


@app.route('/ppt_test', methods=['POST','GET'])
def ptt_test():
    print("ppt_test")
    try:
        content = ptt_beauty()
        #print("content :"+content)
    except InvalidSignatureError:
        abort(400)
    return 'OK'
    
@app.route('/oil_price', methods=['POST','GET'])
def oil_price():
    print("oil_price")
    try:
        content = get_oil_price()
        print("content :"+content)
        line_bot_api.push_message(to, TextSendMessage(text=content))
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@app.route('/stock_price', methods=['POST','GET'])
def stock_price():
    #stockID = request.args.get("stockID")
    stockID = request.get_json().get('stockID', '')
    print(stockID)
    #print(data)
    #print(data.get('stockID', ''))
    text = "2330股價"
    id = text.split("股價")
    print("id:")
    print(id[0])
    stockID = id[0]

    try:
        content = get_stock_price(stockID)
        content = '{}\n{}\n{}\n'.format('股票代號 : ' + content['股票代號'],'公司簡稱 : ' + content['公司簡稱'], '當盤成交價 : ' + content['當盤成交價'])
        print('content :')
        print(content)
        line_bot_api.push_message(to, TextSendMessage(text=content))
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@app.route('/address', methods=['POST','GET'])
def address_to_location():
    geolocator = Nominatim()
    location = geolocator.geocode("台北火車站")
    print(location.address)
    return 'OK'

def get_oil_price():
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
    print("oil title :", title)
    print("gas_price :", gas_price)
    print("oil_price:")
    print(content)
    return content
    #try:
    #    line_bot_api.push_message(to, TextSendMessage(text=content))
    #except LineBotApiError as e:
        # error handle
    #    raise e

def get_stock_price(id):
    #https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_1102.tw
    #target_url = 'https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_'+ id + '.tw'
    print('id :',id)
    target_url = 'https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_'+ id + '.tw&json=1&delay=0'
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    content = json.loads(res.text)
    print('content :')
    print(content)
    data = content['msgArray'][0]
    print('data :')
    print(data)
    print(data['ch'])
    meta = { '股票代號': data['ch'],
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

def get_page_number(content):
    start_index = content.find('index')
    end_index = content.find('.html')
    page_number = content[start_index + 5: end_index]
    return int(page_number) + 1


def parse_article_entries(doc):
    html = HTML(html=doc)
    post_entries = html.find('div.rent')

def parse_article_meta(res):

    soup = BeautifulSoup(res.text, 'html.parser')

    return {
        'title': soup.find('div.title', first=True)
    }


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
    send_Carousel_template_msg(info)               
                
    return "200"

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

def ptt_beauty2():
    print("ptt_beauty")
    rs = requests.session()
    res = rs.get('https://www.ptt.cc/bbs/Beauty/index.html', verify=False, cookies={'over18':'1'})
    #print(res.text)
    soup = BeautifulSoup(res.text, 'html.parser')
    #all_page_url = soup.select('.btn.wide')[1]['href']
    #all_page_url = soup.select("div.title")
    all_page_url = soup.select("div.r-ent")
    #print("all_page_url :" + str(all_page_url))
    
    for entry in all_page_url:
        #print("entry :")
        #print(entry)
        #print(entry.find('a').text)
        #print(entry.find('a').attrs['href'])
        #print("meta :")
        #print(entry.find('div', 'meta'))
        meta = { 'title': entry.find('a').text,
                'link':entry.find('a').attrs['href'],
                'author':entry.find('div', 'meta').find('div','author').text
                
        }
        #meta = parse_article_meta(entry)
    
        if meta is not None:
            print("meta :")
            print(meta)

    """ start_page = get_page_number(all_page_url)
    page_term = 2  # crawler count
    push_rate = 10  # 推文
    index_list = []
    article_list = []
    for page in range(start_page, start_page - page_term, -1):
        page_url = 'https://www.ptt.cc/bbs/Beauty/index{}.html'.format(page)
        index_list.append(page_url)

    # 抓取 文章標題 網址 推文數
    while index_list:
        index = index_list.pop(0)
        res = rs.get(index, verify=False)
        # 如網頁忙線中,則先將網頁加入 index_list 並休息1秒後再連接
        if res.status_code != 200:
            index_list.append(index)
            # print u'error_URL:',index
            # time.sleep(1)
        else:
            article_list = craw_page(res, push_rate)
            # print u'OK_URL:', index
            # time.sleep(0.05)
    content = ''
    for article in article_list:
        data = '[{} push] {}\n{}\n\n'.format(article.get('rate', None), article.get('title', None),
                                             article.get('url', None))
        content += data

    print("content", +content) 
    return content """
    return "200"

def send_Carousel_template_msg(info):

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

    '''CarouselColumns.append(CarouselColumn(
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
                ))'''


    carousel_template_message = TemplateSendMessage(
        alt_text='Carousel template',
        template=CarouselTemplate(
            columns= msg
        )
    )            

    try:
        line_bot_api.push_message(to, carousel_template_message)
    except LineBotApiError as e:
        # error handle
        raise e

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("event.reply_token:", event.reply_token)
    print("event.message.text:", event.message.text)
    #msg = msg.encode('utf-8')

    
    if event.message.text == "PTT 表特版 近期大於 10 推的文章":
        content = ptt_beauty()
        send_Carousel_template_msg(content)
        #line_bot_api.reply_message(
        #    event.reply_token,
        #    TextSendMessage(text=content))
        return 0
    elif event.message.text == "油價":
        content = oil_price()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

    #line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))    

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,debug=True)