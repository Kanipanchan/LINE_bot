from flask import Flask, request, abort
from linebot import WebhookHandler, LineBotApi
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import requests
from linebot.exceptions import InvalidSignatureError
from datetime import datetime


app = Flask(__name__)

# LINE Messaging APIの設定
LINE_CHANNEL_SECRET = 'your_SECRET'
LINE_CHANNEL_ACCESS_TOKEN = 'your_bot_TOKEN'

# OpenWeatherMap APIの設定
OPENWEATHERMAP_API_KEY = 'your_API_key'

# LINE Botのインスタンスを作成
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# LINE Messaging APIからのWebhook
@app.route("/callback", methods=['POST'])
def callback():
    try:
        signature = request.headers['X-Line-Signature']
        body = request.get_data(as_text=True)
        app.logger.info("Request body: " + body)

        # LINE Messaging APIからのリクエストが正当かチェック
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    except Exception as e:
        # 未処理の例外が発生した場合、詳細なエラーメッセージを出力
        app.logger.error(f"Unhandled exception: {str(e)}")
        abort(500)

    return 'OK'


# LINE Botへのメッセージイベントのハンドリング
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text

    if user_message.lower() == "天気":
        # 天気情報を取得
        weather_info = get_weekly_weather()

        # ユーザーに天気情報を返信
        reply_message = f"今日の天気: {weather_info}"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))

# 天気情報をOpenWeatherMap APIから取得
import requests

import requests

def get_weekly_weather(city):
    api_url = 'api.openweathermap'#各自設定
    params = {
        'q': city,  # 取得したい都市名
        'appid': OPENWEATHERMAP_API_KEY,
        'units': 'metric'  # 温度を摂氏で取得
    }

    response = requests.get(api_url, params=params)
    weather_data = response.json()

    if 'list' in weather_data:
        weekly_weather = []
        for data in weather_data['list']:
            timestamp = data['dt']
            date = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            temperature = data['main']['temp']
            weather_description = data['weather'][0]['description']

            # 絵文字のマッピング
            emoji_mapping = {
                'clear sky': '☀️',
                'few clouds': '🌤️',
                'scattered clouds': '⛅',
                'broken clouds': '☁️',
                'shower rain': '🌦️',
                'rain': '🌧️',
                'thunderstorm': '⛈️',
                'snow': '❄️',
                'mist': '🌫️'
                # 他にも必要ならば追加してください
            }

            # 天気説明に対応する絵文字を取得（デフォルトは '❓'）
            emoji = emoji_mapping.get(weather_description, '❓')

            weekly_weather.append(f'{date}: 天気: {weather_description} {emoji}, 気温: {temperature} ℃')

        return weekly_weather
    else:
        return '週間天気情報が取得できませんでした'

    
# LINE Botへのメッセージイベントのハンドリング
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text

    if user_message.lower() == "天気":
        # 週間天気情報を取得（Tokyoを指定していますが、任意の都市を指定してください）
        weekly_weather_info = get_weekly_weather('Tokyo')

        # ユーザーに天気情報を返信
        reply_message = "週間天気: {}".format('\n'.join(weekly_weather_info))
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))


# Tokyoの天気情報を取得
result = get_weekly_weather("Tokyo")
print(result)


if __name__ == "__main__":
    app.run(port=3000)
