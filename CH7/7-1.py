import json

responseJson = {
    "candidates": [
        {
            "content": {
                "parts": [
                    {
                        "text": "為了計算這家公司本月的總利潤，我們需要先計算總收入和總成本，然後用總收入減去總成本。\n\n**1. 計算總收入 (Total Revenue)**\n\n* **A 產品收入：**\n   售價：每件 20 元\n   銷售量：500 件\n   收入 = 售價 × 銷售量 = 20 元/件 × 500 件 = 10000 元\n\n* **B 產品收入：**\n   售價：每件 30 元\n   銷售量：300 件\n   收入 = 售價 × 銷售量 = 30 元/件 × 300 件 = 9000 元\n\n* **C 產品收入：**\n   售價：每件 40 元\n   銷售量：200 件\n   收入 = 售價 × 銷售量 = 40 元/件 × 200 件 = 8000 元\n\n* **總收入：**\n   總收入 = A 產品收入 + B 產品收入 + C 產品收入\n   總收入 = 10000 元 + 9000 元 + 8000 元 = 27000 元\n\n**2. 計算總成本 (Total Cost)**\n\n* **A 產品生產成本：**\n   成本：每件 12 元\n   生產量：500 件\n   成本 = 成本價 × 生產量 = 12 元/件 × 500 件 = 6000 元\n\n* **B 產品生產成本：**\n   成本：每件 18 元\n   生產量：300 件\n   成本 = 成本價 × 生產量 = 18 元/件 × 300 件 = 5400 元\n\n* **C 產品生產成本：**\n   成本：每件 25 元\n   生產量：200 件\n   成本 = 成本價 × 生產量 = 25 元/件 × 200 件 = 5000 元\n\n* **總生產成本：**\n   總生產成本 = A 產品生產成本 + B 產品生產成本 + C 產品生產成本\n   總生產成本 = 6000 元 + 5400 元 + 5000 元 = 16400 元\n\n* **總成本：**\n   總成本 = 總生產成本 + 固定成本\n   總成本 = 16400 元 + 8000 元 = 24400 元\n\n**3. 計算總利潤 (Total Profit)**\n\n* **總利潤：**\n   總利潤 = 總收入 - 總成本\n   總利潤 = 27000 元 - 24400 元 = 2600 元\n\n**結論：**\n\n這個月公司的總利潤是 **2600 元**。\n\n**最終答案：2600**"
                    }
                ],
                "role": "model"
            },
            "finishReason": "STOP",
            "index": 0
        }
    ],
    "usageMetadata": {
        "promptTokenCount": 139,
        "candidatesTokenCount": 676,
        "totalTokenCount": 815,
        "promptTokensDetails": [
            {
                "modality": "TEXT",
                "tokenCount": 139
            }
        ]
    },
    "modelVersion": "gemini-2.0-flash-thinking-exp-01-21"
}

text = responseJson["candidates"][0]["content"]["parts"][0]["text"]
print(text)
