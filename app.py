import os
import google.generativeai as genai
from flask import Flask, request, render_template
from itertools import cycle

app = Flask(__name__)

# 從 Render 的環境變數中讀取 API Key
api_key = os.environ.get("GEMINI_API_KEY")

# 檢查 Key 是否存在
if not api_key:
    print("錯誤：未設定 GEMINI_API_KEY 環境變數")
else:
    genai.configure(api_key=api_key)

# 輪詢不同的模型版本 (免費額度是分開算的)
MODELS_TO_USE = [
    "gemini-2.0-flash", 
    "gemini-1.5-flash", 
    "gemini-1.5-flash-8b"
]
model_pool = cycle(MODELS_TO_USE)

def get_ai_translation(text):
    for _ in range(len(MODELS_TO_USE)):
        current_model_name = next(model_pool)
        try:
            model = genai.GenerativeModel(current_model_name)
            # 加上 System Instruction 限制輸出的簡潔度
            prompt = f"你是一個中韓翻譯專家。請翻譯以下內容（中翻韓或韓翻中），只需給出翻譯結果：{text}"
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"嘗試使用 {current_model_name} 時出錯: {e}")
            continue
    return "目前所有模型都無法使用，請稍後再試。"

# ... 剩下的 @app.route 部分保持不變 ...

if __name__ == '__main__':
    # Render 會自動指定 PORT，所以改用 os.environ.get 獲取
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
