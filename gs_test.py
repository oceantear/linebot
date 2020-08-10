import gspread
import time
import os
import httplib2
from apiclient import discovery
from oauth2client.file import Storage
from oauth2client import client
from oauth2client import tools
from oauth2client.service_account import ServiceAccountCredentials 
#line api
from linebot import LineBotApi

from linebot.models import (
    TextSendMessage, ImageSendMessage, TemplateSendMessage, ButtonsTemplate, PostbackAction, MessageAction, URIAction,
    CarouselTemplate, CarouselColumn, LocationSendMessage, AudioSendMessage, StickerSendMessage, VideoSendMessage)
from linebot.exceptions import LineBotApiError

import requests
from demo.demo_fun import Demo


CHANNEL_ACCESS_TOKEN = "xwYcIrRNGmj7SKJGpl2DSe+GdJ6JEFQXdoBTaVGLkNGPVdTrSTBKeDDxH3CJzK2eTfgIHHq60evtHvhWF1ldXa2h5SKXyMQKEiSVnpDQuxhzC9lwPTqYaSV88lMmGqxolbQrKgOTBMqLO2yjfM71cQdB04t89/1O/w1cDnyilFU="
to = "U2fce467c4cae2847a7d19d631a387782"
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)

def auth_gss_client(path, scopes):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(path, scopes)
    return gspread.authorize(credentials)

def getCredentials():
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
    CLIENT_SECRET_FILE = 'client_secret.json'
    #CLIENT_SECRET_FILE = 'auth.json'
    APPLICATION_NAME = 'Google Sheets API Python Quickstart'
    flags = None
    try:
        import argparse
        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    except ImportError:
        flags = None
    print("flags :")
    print(flags)
    # 授權目錄
    #credential_dir = '.credentials'
    credential_dir = '.'

    # 取得授權紀錄
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'sheets.googleapis.com-python-quickstart.json')
    #credential_path = os.path.join(credential_dir, CLIENT_SECRET_FILE)
    store = Storage(credential_path)
    credentials = store.get()

    # 判斷是否有授權紀錄或是受全是否失效，若沒有或失效則重新或取授權並儲存授權
    if not credentials or credentials.invalid:
        clientsecret_path = os.path.join(credential_dir, CLIENT_SECRET_FILE)
        print("credentail path :"+clientsecret_path)
        flow = client.flow_from_clientsecrets(clientsecret_path, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials    

def getSheetValue(spreadsheetId, rangeName):
    # 建立 Google Sheet API 連線
    credentials = getCredentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?''version=v4')
    #service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)
    service = discovery.build('sheets', 'v4', credentials=credentials)
    # 取的 Sheet 資料
    result = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])

    return values    

auth_json_path = 'auth.json' #由剛剛建立出的憑證，放置相同目錄以供引入
gss_scopes = ['https://spreadsheets.google.com/feeds'] #我們想要取用的範圍
gss_client = auth_gss_client(auth_json_path, gss_scopes) #呼叫我們的函式

def gen_Carousel_template_msg(info):

    msg = list()
    for data in info:
        print("title :", data.get('title'))
        #print("link :", "https://www.ptt.cc" + data.get('addr'))
        print("Imgurl :", data.get('img_url'))
        url = data.get('url')
        msg.append(CarouselColumn(
                        thumbnail_image_url= data.get('img_url'),
                        title=data.get('title'),
                        text=data.get('title'),
                        actions=[
                            URIAction(
                                label='點擊看食記',
                                uri=url
                            )
                        ]
                    ))
    return msg



#從剛剛建立的sheet，把網址中 https://docs.google.com/spreadsheets/d/〔key〕/edit 的 〔key〕的值代入 
spreadsheet_key_path = '1dcVq9JvBY_qloGWpPzuWu16QvxiGrKrkWEmI5oJ24KQ'

#我們透過open_by_key這個method來開啟sheet
sheet = gss_client.open_by_key(spreadsheet_key_path).sheet1
#單純取出時間稍後塞入sheet
#today = time.strftime("%c")
#透過insert_row寫入值 第二行塞入時間,abc,123的值
#sheet.insert_row([today,"abc", 123], 2)

print("record:")
lunch_data = list()
list_of_lists = sheet.get_all_values()
for data in list_of_lists:
    print(data)
    print(data[0])
    item = dict()
    item['title']=data[0]
    item['address']=data[1]
    item['img_url']=data[2]
    item['url']=data[3]
    lunch_data.append(item)

print("lunch_data :")
print(lunch_data)    

msg = gen_Carousel_template_msg(lunch_data)

carousel_template_message = TemplateSendMessage(
        alt_text='午餐吃什麼',
        template=CarouselTemplate(
            columns= msg
        )
    )
try:
        line_bot_api.push_message(to, carousel_template_message)
except LineBotApiError as e:
        # error handle
        raise e            
