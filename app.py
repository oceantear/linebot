from flask import Flask, request, abort

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


    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))    

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,debug=True)