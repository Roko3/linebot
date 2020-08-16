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

app = Flask(__name__)

# Line Bot APIのインスタンス
linebot_api = LineBotApi('+FD33MxyHhY96+T7LQB9Wv446bC62FBWXwsFV62oa2bV6T/HS7FnxX\
6b8iuzJr7HS+5318y2VtugkGCfPcp8ewJ5VIMpB6xNlUaGbw4T/RCFMSjuMv4QbccRcbpS+pjUTyHnYTceaNSocKo5faP3cgdB04t89/1O/w1cDnyilFU=')

handler = WebhookHandler('41402ebb24790567860c3b07a5305298')  # 送られてきたメッセージを扱うハンドラ


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

@handler.add(MessageEvent,message=TextMessage)
def handle_message(event):
  ai_message = talk_ai(event.message.text)

  linebot_api.reply_message(event.reply_token, TextSendMessage(text = ai_message))

def talk_ai(word):
  apikey = "DZZRDEzj6wXxRkI6CZB2ziJz69TcOR6h"
  client = pya3rt.TalkClient(apikey)
  reply_message=client.talk(word)

  return reply_message['results'][0]['reply']


if __name__ == '__main__':
  app.run()

