# 匯入Loading API所需的程式庫
from linebot.v3.messaging import ShowLoadingAnimationRequest

line_bot_api = MessagingApi(api_client)

# 顯示載入動畫
line_bot_api.show_loading_animation(ShowLoadingAnimationRequest(chatId=event.source.user_id, loadingSeconds=30))
