import win32com.client, re, requests, pythoncom
from flask import Flask, request, Response, jsonify
from pyngrok import ngrok, conf
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def extract_digits(text):
    # 正規表現を使用して数字のみを抽出します
    digits = re.findall(r'\d{8}', text)
    if digits:
        # 数字のみを取り出して文字列として結合します
        digits_str = ''.join(digits)
        return digits_str
    else:
        return None


def GetCode():
    outlook = win32com.client.Dispatch("Outlook.Application",pythoncom.CoInitialize()).GetNamespace("MAPI")
    account = outlook.Folders[0]
    folder = account.Folders[6]
    mails = folder.Items
    for mail in mails:
        if mail.Unread:
            mail.Unread = False
            return extract_digits(mail.body)
    return None


@app.route('/')
def main():
    print("start to get")
    count = 0
    while count < 100:  # 5回試行する例として設定
        result = GetCode()
        if result:
            print("verification code : ", result)
            return jsonify({"verification_code": result})
        count += 1
    return jsonify({"error": "Verification code not found"})

if __name__ == "__main__":
    public_url = ngrok.connect(5000)
    print(f"ngrok URL: {public_url}")
    app.run(port=5000)
