from ollama import ChatResponse, chat
model = "llama3.2:3b"

def get_order_status(order_id: str) -> str:
    """
    根據訂單編號取得訂單狀態

    Args:
        order_id (str): 訂單編號

    Returns:
        str: 訂單狀態說明
    """
    # 模擬訂單狀態查詢，實際應用中會連接資料庫或 API 查詢
    order_statuses = {
        "08957": "處理中",
        "88168": "已出貨",
        "77377": "已取消"
    }
    return order_statuses.get(order_id, "查無訂單")

def cancel_order(order_id: str) -> str:
    """
    取消處理中的訂單

    Args:
        order_id (str): 訂單編號

    Returns:
        str: 取消訂單後的結果說明
    """
    # 模擬取消訂單邏輯，實際應用中會更新訂單資料庫記錄
    order_statuses = {
        "08957": "處理中",
        "88168": "已出貨",
        "77377": "已取消"
    }
    current_status = order_statuses.get(order_id)
    if current_status == "處理中":
        return f"訂單 {order_id} 已成功取消"
    elif current_status == "已出貨":
        return f"訂單 {order_id} 已出貨，無法取消"
    else:
        return f"訂單 {order_id} 查無資料或已取消"

# 定義工具的 schema，讓模型了解工具用途與所需參數格式
get_order_status_tool = {
    "type": "function",
    "function": {
        "name": "get_order_status",
        "description": "查詢訂單狀態，回傳訂單當前狀態",
        "parameters": {
            "type": "object",
            "required": ["order_id"],
            "properties": {
                "order_id": {"type": "string", "description": "訂單編號"}
            }
        }
    }
}

cancel_order_tool = {
    "type": "function",
    "function": {
        "name": "cancel_order",
        "description": "取消處理中的訂單",
        "parameters": {
            "type": "object",
            "required": ["order_id"],
            "properties": {
                "order_id": {"type": "string", "description": "訂單編號"}
            }
        }
    }
}

# 建立function name 與function實作的對應關係
available_functions = {
    "get_order_status": get_order_status,
    "cancel_order": cancel_order,
}

# 模擬使用者輸入的訊息，包含查詢訂單狀態與取消訂單的需求
messages = [
    {"role": "system", "content": "你是一位智能訂單服務機器人，服務範圍包含查詢訂單狀態與取消訂單，必須使用繁體中文回答。"},
    {"role": "user", "content": "請問訂單 08957 的狀態是什麼？"},
    {"role": "user", "content": "如果可以的話，請取消訂單 55666"}
]

print("使用者訊息:", messages)

# 呼叫模型，並將工具（包含直接的函式與工具 schema）一併傳入
response: ChatResponse = chat(
    model=model,
    messages=messages,
    tools=[get_order_status_tool, cancel_order_tool],
)



# 處理模型回傳的工具呼叫結果
if response.message.tool_calls:
    for tool in response.message.tool_calls:
        func_name = tool.function.name
        print("\n\n模型呼叫函數:", func_name)
        print("呼叫參數:", tool.function.arguments)
        if (func_to_call := available_functions.get(func_name)):
            try:
                result = func_to_call(**tool.function.arguments)
                print("函數執行結果:", result)
            except Exception as e:
                print("執行函數時發生錯誤:", e)
        else:
            print("找不到對應函數:", func_name)
    
    # 將工具回應加入對話訊息中，並與模型再次互動以獲得最終回覆
    messages.append(response.message)
    messages.append({
        "role": "tool",
        "name": tool.function.name,
        "content": str(result)
    })
    final_response = chat(model, messages=messages)
    print("最終模型回應:", final_response.message.content)
else:
    print("模型未返回任何工具呼叫")
