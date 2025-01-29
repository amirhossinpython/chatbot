from flask import Flask, request, jsonify, render_template
import requests
from datetime import datetime
from khayyam import JalaliDatetime
import random

app = Flask(__name__)


def get_jalali_time():
    
    return JalaliDatetime.now().strftime('%Y/%m/%d - %H:%M')


predefined_responses = {
    "زمان": get_jalali_time,
    "چنل": lambda: "بفرما چنل ما: @Python_Source_1403"
}

def get_response_from_api(user_input):
    url = "https://api.api-code.ir/gpt-4/"
    payload = {"text": user_input}
    
    try:
        response = requests.get(url, params=payload)
        response.raise_for_status() 
        data = response.json()
        return data['result']
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

# API 2: GPT-4 from Haji API
def get_chat_4(text):
    link = f"https://api3.haji-api.ir/lic/gpt/4?q={text}&license=dyEe1vk0CvCg5ibb0bI62XP3tuVeDtHdz9AK3dREoTxwgKkUX"
    
    try:
        res = requests.get(link)
        res.raise_for_status()  # بررسی وضعیت پاسخ
        result = res.json().get("result")
        return result if result else "No result found"
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

@app.route('/')
def index():
    """نمایش صفحه اصلی."""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """دریافت پیام کاربر و ارسال پاسخ."""
    user_message = request.json.get('message', '').strip()  # پیام کاربر
    # انتخاب تصادفی یکی از دو API
    get_result = random.choice([get_response_from_api, get_chat_4])

    if not user_message:
        return jsonify({
            'user_message': user_message,
            'response_message': 'لطفاً یک پیام معتبر وارد کنید.',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

    # بررسی پیام‌های از پیش تعریف شده
    if user_message in predefined_responses:
        response_message = predefined_responses[user_message]()
    else:
        response_message = get_result(user_message)
    
    return jsonify({
        'user_message': user_message,
        'response_message': response_message,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

if __name__ == '__main__':
    app.run(debug=True)
