# -*- coding: utf-8 -*-
"""line_bot.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_XjtvdESphj99Upg4o2q_h92inFbGb6D
"""

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent,TextMessage,TextSendMessage
import pya3rt

import re, json, requests

app = Flask(__name__)

# Line Bot APIのインスタンス
linebot_api = LineBotApi('wBrEz3r02T2Oe3syQRscSmZcjmnp261gmaVYGyKGMzFNeBeF4M7kNLx\
                          /uFMkLVSAFC0RHUKphM4VComJ9TtwRsh4Kh1Sn2SNbWInMmr6RWqzbs\
                          mRtTGP++1lCYnxj+cfCIEZ9ZOEyvqrTVWeD9mx3gdB04t89/1O/w1cDnyilFU=')

handler = WebhookHandler('c7e1bc08e54a0ff52932a9cc3dd25a51')  # 送られてきたメッセージを扱うハンドラ


@app.route('/callback',methods=['POST'])
def callback():

  # リクエストがLINE Platformから送られてきたのかを確認する
  signature = request.headers["X-Line-Signature"] # サインを取り出す
  body = request.get_data(as_text=True)         # ボディも取り出す

  '''
  Webhookとはイベントが行われた時にイベントを処理するサーバーへイベントを送るためのものです
  LINEの場合、イベントというのは、友だち追加やメッセージの送信などを指します。

  tryexcept文を使ってイベントがLINEPlatformから送られたものであれば、
  WebhookHandlerを呼び出してイベントを処理し、
  送られたものでなければ、リクエストを中断してHTTPステータスコードの『400番』を返すような記述をしましょう。
  '''
  try:
    handler.handle(body,signature)    # LINEPlatformから送られたもの

  except InvalidSignatureError:
    abort(400)

  return 'OK'

##*****************************************************
# mesaage handler
#******************************************************
@handler.add(MessageEvent,message=TextMessage)
def handle_message(event):
    
  print(event.message.text)   

  # 7桁の数字を探す
  # もし機種名があれば、取り出す

  # 5216000&model=SR7500'

  send_message = event.message.text  # 送られてきたメッセージ

  error_code_regex = re.compile(r'["0-9"A-Fa-f]{7}')    # 0-9,A-F,a-fで入力された７桁の文字列を探す
  mo = error_code_regex.search(send_message)            # 検索する

  if mo:                          # 検索文字があれば
    error_code = mo.group()       # 検索文字を取り出す

    if 'SR' in send_message or 'sr' in send_message:
      machine_model = 'SR7500'
    elif 'VS' in send_message or 'vs' in send_message:
      machine_model = 'VS-ATM'
    elif 'TCR' in send_message or 'tcr' in send_message:
      machine_model = 'TCR'
    else:
      machine_model = 'SR7500'
    
    # find error code
    unit, title, contents, detail, recovery = get_error_detail(machine_model,error_code)

    if unit:

      ai_message = "Machine model :  " + machine_model \
                    + "\nError code : " + error_code \
                    + "\n\nUnit : " + unit \
                    + "\n\nTitle : " + title \
                    + "\n\nContents : " + contents \
                    + "\n\nDetail : " + detail \
                    + "\n\nRecovery : " + recovery

    else:
      ai_message = "not find the error code : " + error_code

  else:
    ai_message = "Please give me error code and machine model\n \
                  ex.'SR, 5216000'\n \
                  'tell me 5216000 VS"

    #ai_message = talk_ai(send_message)

  linebot_api.reply_message(event.reply_token, TextSendMessage(text = ai_message))



##*****************************************************
# responsed by AI
#******************************************************
def talk_ai(word):
      
  apikey = "DZZRDEzj6wXxRkI6CZB2ziJz69TcOR6h"
  client = pya3rt.TalkClient(apikey)
  reply_message=client.talk(word)

  return reply_message['results'][0]['reply']



##*****************************************************
# get error code detail from HOTS-JP site
#******************************************************
def get_error_detail(machine_model, error_code):
      
  unit = title = contents = detail = recovery = None

  # URLをセットする
  url = 'https://app.hitachi-omron-ts.com/api/ErrorCodes00/ecs?code=' + error_code + '&model=' + machine_model

  # Web-APIをアクセスする
  response = requests.get(url)

  # <Response [200]>
  # エラーをチェックする（例外が発生しなければ正常）
  response.raise_for_status()

  # データを取り出す
  data = json.loads(response.text)

  if data:
    unit = data[0]["Unit"]
    title = data[0]["Title"]
    contents = data[0]["Contents"]
    detail = data[0]["Detail"]
    recovery = data[0]["Recovery"]

  return unit, title, contents, detail, recovery



if __name__ == '__main__':
  app.run()
