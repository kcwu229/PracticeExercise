import line_token             # for line bot authorization
from flask import Flask       # web-frame
app = Flask(__name__)

from flask import request, abort   # return message message to html -- similar to raise error
from linebot import LineBotApi, WebhookHandler   # Line API 
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

line_bot_api = LineBotApi(line_token.channel_access_token)
handler = WebhookHandler(line_token.channel_secret)

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))

if __name__ == "__main__":
    app.run()