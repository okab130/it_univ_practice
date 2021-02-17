from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('6N5C6SGqMRtzSOS9ggWEjlD9gMH7l5JxCXERwothBD+yzRoVquCT9Uo26DZbEGPnfXVzyO87cNXqWrLdAeONKHHJdhgQg5jOzvCMRoXjIw12sKsFX9TPktQI1EeHn849twzC32+SUJBkMWJ6eay4IwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('9bbf9aae9947348e6227831f0f750125')

@app.route("/")
def test():
    return "OK"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == "ありがとさん":
        reply_message="どういたしまして"
    else:
        reply_message=f"あなたは、{event.message.text}と言いました"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message))


if __name__ == "__main__":
    app.run()
