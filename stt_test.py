import speech_recognition as sr

def recognize_speech_from_mic():
    """
    マイクから音声を取得し、テキストに変換して返します。
    """
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    print("マイクの準備中...")
    
    try:
        with microphone as source:
            # 周囲のノイズに合わせて調整
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("なにか話してください...")
            
            # 音声を聞き取る
            audio = recognizer.listen(source)

        print("解析中...")
        # Google Web Speech APIを使用して認識（日本語に設定）
        text = recognizer.recognize_google(audio, language="ja-JP")
        return text

    except sr.RequestError:
        # APIが利用できない場合
        return "APIが利用できません。インターネット接続を確認してください。"
    except sr.UnknownValueError:
        # 音声が認識できなかった場合
        return "音声が認識できませんでした。"
    except Exception as e:
        return f"エラーが発生しました: {e}"

if __name__ == "__main__":
    result = recognize_speech_from_mic()
    print(f"認識結果: {result}")
