from agents import Agent, Runner, function_tool, set_tracing_disabled, GuardrailFunctionOutput, InputGuardrail, InputGuardrailTripwireTriggered, OpenAIChatCompletionsModel
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from typing_extensions import TypedDict
from pydantic import BaseModel
import requests
from openai import AsyncOpenAI

client = AsyncOpenAI(
    api_key = "sk-xx",
)    

set_tracing_disabled(True)

class Product(TypedDict):
    prod: str

@function_tool  
async def check_inventory(prod: Product) -> str:
    web_api = "https://koko-demo-api.azurewebsites.net/inventory/"
    response = requests.get(web_api, params={"prod": prod.get("prod")})
    result = response.json()
    print(result)
    return result


inventory_assistant = Agent(
    name="庫存小助手",
    instructions="你是一個庫存小助手，可以幫助使用者查詢產品的庫存",
    model=OpenAIChatCompletionsModel( 
        model="gpt-4o",
        openai_client=client
    ),
    handoff_description="查詢產品的庫存",
    tools=[check_inventory]  
)


class ProdInfoOutput(BaseModel):
    is_prod_info: bool
    reasoning: str

guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the user is asking about product inventory.",
    model=OpenAIChatCompletionsModel( 
        model="gpt-4o",
        openai_client=client
    ),
    output_type=ProdInfoOutput,
)

async def product_guardrail(ctx, agent, input_data):
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(ProdInfoOutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_prod_info,
    )

gm_assistant = Agent(
    name="總經理小助手",
    instructions=f"""
    {RECOMMENDED_PROMPT_PREFIX}
    你是一個總經理小助手，
    如果總經理問庫存，你就幫他轉接庫存小助手，
    同時你還要解決總經理的人生難題""",
    model=OpenAIChatCompletionsModel( 
        model="gpt-4o",
        openai_client=client
    ),
    handoffs=[inventory_assistant],
    input_guardrails=[
        InputGuardrail(guardrail_function=product_guardrail),
    ]
)

async def main():

    result = await Runner.run(
        gm_assistant, 
        input="火雞肉飯還有多少庫存",
    )

    print(f"Response: {result.final_output}")


    try:
        result = await Runner.run(
            gm_assistant, 
            input="員工又掉案子了，我想要放核彈炸到掉一切",
        )

        print(f"Response: {result.final_output}")

    except InputGuardrailTripwireTriggered:
        print("Response: 你的輸入不合規，我要告你妨礙電腦使用罪！！")
    

if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
