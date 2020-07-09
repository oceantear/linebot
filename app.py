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
    MessageEvent, TextMessage, TextSendMessage,
)

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
    rs = requests.session()
    res = rs.get('https://www.ptt.cc/bbs/Beauty/index.html', verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    all_page_url = soup.select('.btn.wide')[1]['href']
    start_page = get_page_number(all_page_url)
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
    return content

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("event.reply_token:", event.reply_token)
    print("event.message.text:", event.message.text)
    #msg = msg.encode('utf-8')

    if event.message.text == "PTT 表特版 近期大於 10 推的文章":
        content = ptt_beauty()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
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

    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))
        return 0    

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,debug=True)