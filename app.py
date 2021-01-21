from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import os

app = Flask(__name__)


self_intro = '''我是柯宏穎，目前就讀於臺大資工系大四，同時也雙主修經濟。我從大一開始接觸程式，雖然開始的時間比別人晚了一些，但也因為如此，我比其他同學更加努力，就為了跟上大家的腳步，甚至超越他們。大學修課期間，令我較有興趣且有些深入研究的有深度學習、Computer Vision 及data processing相關，目前也於系上 CMLab 進行醫療資料的分析與處理。
這學期為了充實自己，選了自己從未接觸的前後端網路服務課程，中間獲益良多，從無到有假設了一個教學課程平臺，雖然辛苦，卻也成就感十足。我個性隨和好相處，在學校與大家分組作業時，我都有良好的開發經驗與互動。
平時閒暇時間，我都會待在系館，和大家一起討論作業、休息遊樂，在討論過程中，常可以學習各位強者的想法與思考邏輯，讓我那我能在日常生活中進步。非常希望能有機會進入貴公司學習與發展，去學習與瞭解一個眾多人在使用的應用程式背後的開發與架構，也去學習在學校學不到的軟體開發流程，增加職場經驗，提升自己的競爭力。'''

works = '''ASUS AICS software summer intern
    Jul 2019 ~ Aug 2019:
        Work Study and work with the Computer Vision team.

ASUS AICS software summer intern
    Jul 2020 ~ Aug 2020:
        Work Study and work with the Computer Vision retial team.

2020 NTU CSIE Camp VR course lecturer
    Jul 2020 ~ Jul 2020
        Introduction to Virtual Reality for high school students.

NTU CSIE Lab Research Student
    Feb 2020 - Present
        Research and work with seniors in CMLab. Corporate with the Medical team. Work on Liver Cancer & Jaundice data analysis.'''

skills = '''C/C++ Language
Python
Verilog
Shell Script
R
Linux Administration
Machine Learning
React.js
HTML/CSS'''

experience = '''Shopee, I’m The Best Coder ! Challenge 2020 - 3rd Place
    Nov 2020
        Solving complicated business data analysis problems in the contest. Standout in 50+ teams and won the prize.'''

transcript_url = "https://i.imgur.com/nkwpzE2.jpg"

default = '''歡迎輸入以下指令來看我的個人資訊呦（輸入數字即可）：
1. 自我介紹
2. 工作經歷
3. 程式語言能力
4. 相關比賽經驗
5. 成績單'''

table = {"default": default, "1": self_intro, "2": works, "3": skills, "4": experience}
valid = ["1", "2", "3", "4", "5"]

def transform(op):
    if op not in valid:
        return "default"
    return op

# Channel Access Token
line_bot_api = LineBotApi(os.getenv("ACCESS_TOKEN"))
# Channel Secret
handler = WebhookHandler(os.getenv("SECRET"))

# 監聽所有來自 /callback 的 Post Request
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
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    option = transform(event.message.text)
    if (option == "5"):
        message = ImageSendMessage(
            original_content_url=transcript_url,
            preview_image_url=transcript_url
        )
    else:
        message = TextSendMessage(text=table[option])
    
    line_bot_api.reply_message(event.reply_token, message)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
