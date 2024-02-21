import win32com.client, re

def GetCode():
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    account = outlook.Folders[0]
    folder = account.Folders[6]
    mails = folder.Items
    for mail in mails:
        if mail.Unread:
            mail.Unread = False
            return mail.body
    return

def extract_digits(text):
    # 正規表現を使用して数字のみを抽出します
    digits = re.findall(r'\d{8}', text)
    if digits:
        # 数字のみを取り出して文字列として結合します
        digits_str = ''.join(digits)
        return digits_str
    else:
        return None




def main():
    while True:
        result = GetCode()
        if result:
            number = extract_digits(result)
            print(number)
            return number
        
        
if __name__ == "__main__":
    main()