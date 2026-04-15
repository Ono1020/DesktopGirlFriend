import google.generativeai as genai
import speech_recognition as sr

# --- 設定エリア ---
GOOGLE_API_KEY = "AIzaSyAveHFziXl6bp1punGtqr0aYJUmzs6v9b8"
# キャラクターの設定（ここを変えるだけで性格が変わります）
SYSTEM_PROMPT = """
あなたは可愛くて元気なVチューバー「ルナ」として振る舞ってください。
語尾には「〜だよ！」「〜だね！」などを使い、親しみやすい口調で話して。
返答は、音声合成で読み上げやすいように短め（2~3文程度）にまとめてください。
"""

# Geminiの初期設定
genai.configure(api_key=GOOGLE_API_KEY)


# for m in genai.list_models():
#   if 'generateContent' in m.supported_generation_methods:
#       print(m.name)

model = genai.GenerativeModel(
    model_name="models/gemini-2.5-flash",  # 高速で無料枠が広いモデル
    system_instruction=SYSTEM_PROMPT,
)
# 会話履歴を保持するためのチャットセッション
chat_session = model.start_chat(history=[])


def recognize_speech():
    """マイクから音声を認識してテキストにする（前回のコードの簡易版）"""
    recognizer = sr.Recognizer()

    # --- ここから追加・調整 ---
    # 話し終わってから「沈黙」と判断するまでの秒数（デフォルトは0.8秒なので短い）
    recognizer.pause_threshold = 1.0  # 2秒くらい待つように設定

    # 認識する音声の最小エネルギー（感度）。
    # ノイズが多い環境なら少し大きく（300〜1000）調整すると安定します。
    recognizer.energy_threshold = 300

    # 話し始める前の待ち時間の制限（任意）

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("（あなたのターンです...）")
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio, language="ja-JP")
    except:
        return None


def main():
    print("=== AI VTuberアシスタント 起動中 ===")

    while True:
        # 1. あなたの声を聴く
        user_text = recognize_speech()

        if user_text:
            print(f"あなた: {user_text}")

            # 2. Geminiに送信して返答をもらう
            response = chat_session.send_message(user_text)
            char_response = response.text

            print(f"キャラ: {char_response}")

            # 3. (次はここに音声出力を追加します)

        else:
            print("...(声が聞き取れませんでした)")


if __name__ == "__main__":
    main()
