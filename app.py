import os
import google.generativeai as genai
from flask import Flask, request, render_template
from itertools import cycle

app = Flask(__name__)

# 從 Render 的 Environment 讀取 API Key
# 記得在 Render 後台設定一個名為 GEMINI_API_KEY 的變數
API_KEY = os.environ.get("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)

# 定義模型池，利用輪詢 (Round Robin) 分散請求壓力
# 這些模型的免費額度通常是獨立計算或有不同的限制
MODELS_TO_USE = [
    "models/gemini-2.0-flash", 
    "models/gemini-1.5-flash", 
    "models/gemini-1.5-flash-8b"
]
model_pool = cycle(MODELS_TO_USE)

def get_ai_translation(text):
    """嘗試調用 AI 進行翻譯，失敗則跳轉下一個模型"""
    if not API_KEY:
        return "系統未設定 API Key，請檢查環境變數。"

    # 最多嘗試與模型數量相同的次數
    for _ in range(len(MODELS_TO_USE)):
        current_model_name = next(model_pool)
        try:
            model = genai.GenerativeModel(
                model_name=current_model_name,
                system_instruction="你是一個專業的中韓翻譯機。請將輸入的文字翻譯成另一種語言（中翻韓，或韓翻中）。只需回傳翻譯結果，不要有任何解釋或贅字。"
            )
            
            response = model.generate_content(text)
            
            # 檢查回應是否包含內容
            if response and response.text:
                return response.text.strip()
                
        except Exception as e:
            print(f"模型 {current_model_name} 調用失敗: {e}")
            continue # 失敗就換下一個
            
    return "抱歉，目前所有 AI 服務忙碌中，請稍後再試。"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['GET', 'POST'])
def ask():
    if request.method == 'POST':
        question = request.form.get('question', '').strip()
        if not question:
            return render_template('ask.html', question="", answer="請輸入內容")
        
        # 呼叫 AI 翻譯函數
        answer = get_ai_translation(question)
        return render_template('ask.html', question=question, answer=answer)
    
    return render_template('ask.html', question="", answer="")

if __name__ == '__main__':
    # Render 會自動指定 PORT，若無則預設 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
