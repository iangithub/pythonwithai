@handler.add(MessageEvent)
def handle_message(event):
    if (event.message.type == "image"):
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)

            # 顯示載入動畫
            line_bot_api.show_loading_animation(ShowLoadingAnimationRequest(chatId=event.source.user_id, loadingSeconds=30))

            # 取得圖片內容並進行Base64編碼
            line_bot_api_blob = MessagingApiBlob(api_client)
            receivedImage = base64.b64encode(line_bot_api_blob.get_message_content(event.message.id)).decode('utf-8')

            # 組合Flex彈性訊息
            flex = {"type":"bubble","size":"giga","body":{"type":"box","layout":"vertical","contents":[{"type":"text","text":"針對這道美食，我想說的是…","size":"xl","align":"center","weight":"bold"},{"type":"separator","color":"#000000","margin":"md"},{"type":"box","layout":"horizontal","contents":[{"type":"image","url":"https://chibu.app/reviewer.jpg","size":"full","aspectRatio":"1:1","flex":1},{"type":"text","text":generate(receivedImage),"gravity":"center","align":"center","adjustMode":"shrink-to-fit","flex":2,"size":"lg","wrap":True,"margin":"md"}],"margin":"md"}]}}

            # 以Flex彈性訊息回覆
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[FlexMessage(alt_text="關於這道美食，我想說的是…", contents=FlexContainer.from_json(json.dumps(flex)))]
                )
            )
    else:
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text="請上傳一張美食照片給我，我可以幫您寫評論喔！")]
                )
            )
