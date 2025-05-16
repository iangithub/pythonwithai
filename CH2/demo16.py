import ollama

class Agent:
    # 通用 AI 代理人類別，封裝角色提示和對應模型調用
    def __init__(self, role_prompt: str, model: str = "hf.co/bartowski/DeepSeek-R1-Distill-Qwen-7B-GGUF:latest"):
        self.role_prompt = role_prompt
        self.model = model

    # 執行代理人的任務：將使用者輸入與角色提示結合，取得模型回應
    def run(self, user_input: str) -> str:
        messages = [
            {"role": "system", "content": self.role_prompt},
            {"role": "user", "content": user_input}
        ]
        # 呼叫本地模型取得回應
        response = ollama.chat(model=self.model, messages=messages)
        return response.message.content.strip()

# 定義代理人角色提示
data_collector_prompt = (
    """
    你是一位市場資料蒐集員，擁有大量行業報告和市場數據。
    你的任務是根據用戶的問題，找出相關的事實、數據和趨勢。
    直接給出你認為最相關的市場資訊要點即可，不需要額外評論。
    """   
)
analyst_prompt = (
    """
    你是一位市場分析師。你將根據提供的市場資料以SWOT分析與PEST分析趨勢並提出見解。
    請深入思考數據所代表的含義，找出問題背後的重要因素，
    並整理出對我們公司的策略建議要點。只需提供分析重點。
    """   
)
reporter_prompt = (
    """
    你是一位專業報告撰寫員。你的工作是將分析師提供的要點寫成結構清晰的報告來回答用戶問題。
    報告應包含市場趨勢概括、分析洞見，以及對策建議，
    語氣專業且易於理解。請根據上述要點撰寫完整回答。
    """   
)

# 建立代理人實例
data_collector_agent = Agent(role_prompt=data_collector_prompt)
analyst_agent = Agent(role_prompt=analyst_prompt)
reporter_agent = Agent(role_prompt=reporter_prompt)

# 處理使用者的查詢，依序調用多個代理人，傳回最終答案。
def answer_question(query: str) -> str:
    collected_info = data_collector_agent.run(query)
    analysis_input = f"以下是市場資料：{collected_info}\n請根據這些資訊進行分析並提出重點。"
    analysis_result = analyst_agent.run(analysis_input)
    report_input = f"分析師提供了以下要點：{analysis_result}\n請將這些要點整理成報告回答用戶問題。"
    final_report = reporter_agent.run(report_input)
    return final_report

if __name__ == "__main__":
    print("歡迎使用市場分析助理系統。請輸入您的問題，輸入 'exit' 可離開。")
    while True:
        user_query = input("\n請輸入分析問題: ")
        if user_query.strip().lower() in ["exit", "quit", "q", "退出"]:
            print("已退出市場分析助理。")
            break
        if not user_query.strip():
            continue
        print("\n問題收到，正在分析請稍候...\n")
        final_answer = answer_question(user_query)
        print("分析助理報告:\n" + final_answer + "\n")
        print("--------------------------------------------------")
        print("可以輸入另一個問題，或輸入 'exit' 結束。\n")
