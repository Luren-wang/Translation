from flask import Flask, request, render_template

app = Flask(__name__)

# 1. 建立「中翻韓」的基礎題庫
base_dict = {
    "你好": "안녕하세요",
    "謝謝": "감사합니다",
    "對不起": "죄송합니다",
    "早安": "좋은 아침",
    "晚安": "안녕히 주무세요",
    "老師": "선생님",
    "學生": "학생",
    "朋友": "친구",
    "家人": "가족",
    "愛": "사랑",
    "是": "네",
    "不是": "아니요",
    "我": "저", 
    "你": "당신",
    "爸爸": "아빠",
    "媽媽": "엄마",
    "水": "물",
    "飯": "밥",
    "麵包": "빵",
    "咖啡": "커피",
    "蘋果": "사과",
    "學校": "학교",
    "公司": "회사",
    "家": "집",
    "今天": "오늘",
    "明天": "내일",
    "昨天": "어제",
    "好吃": "맛있다",
    "漂亮": "예쁘다",
    "開心": "기쁘다",
    "累": "피곤하다"
}

# 2. 自動生成雙向字典
# 先複製一份原本的字典
zh_ko_dict = base_dict.copy() 

# 把基礎題庫裡的值（韓文）當作鍵，鍵（中文）當作值，存回字典裡
for zh, ko in base_dict.items():
    if ko not in zh_ko_dict:
        zh_ko_dict[ko] = zh

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['GET', 'POST'])
def ask():
    if request.method == 'POST':
        # 讀取學生的問題
        question = request.form.get('question', '').strip()
        # 查詢題庫的對應答案 (現在同時支援輸入中文或韓文)
        answer = zh_ko_dict.get(question, "抱歉，我目前沒有這個詞的對應翻譯。")
        # 回傳答案給學生
        return render_template('ask.html', question=question, answer=answer)
    # GET 時給空白欄位
    return render_template('ask.html', question="", answer="")


if __name__ == '__main__':
    app.run(debug=False)
