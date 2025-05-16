# 匯入Get Content API所需的程式庫
from linebot.v3.messaging import MessagingApiBlob
import base64

# 取得圖片內容並進行Base64編碼
line_bot_api_blob = MessagingApiBlob(api_client)
receivedImage = base64.b64encode(line_bot_api_blob.get_message_content(event.message.id)).decode('utf-8')

# 以文字訊息回覆
line_bot_api = MessagingApi(api_client)
line_bot_api.reply_message_with_http_info(
    ReplyMessageRequest(
        reply_token=event.reply_token,
        messages=[TextMessage(text="Base64 Encoded into {0} bytes string".format(len(receivedImage)))]
    )
)
