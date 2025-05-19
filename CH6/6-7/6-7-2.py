import asyncio
import shutil
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled
from agents.mcp import MCPServer, MCPServerStdio

client = AsyncOpenAI(
    api_key = "sk-xx",
)    

set_tracing_disabled(True)

async def run(mcp_server: MCPServer):
    agent = Agent(
        name="Assistant",
        instructions="你要解析user問的產品名稱，使用InventoryAI並且回答庫存問題",
        model=OpenAIChatCompletionsModel( 
            model="gpt-4o",
            openai_client=client
        ),
        mcp_servers=[mcp_server],
    )

    message = "火雞肉飯還有多少庫存？"
    print(f"\n\nRunning: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    print(result.final_output)


async def main():
    async with MCPServerStdio(
        name="InventoryAI",
        params={
            "command": "uv",
            "args": [
                "--directory",
                "<path to your directory>",
                "run",
                "server.py"
            ],
        },
    ) as server:
        await run(server)


if __name__ == "__main__":
    if not shutil.which("uv"):
        raise RuntimeError("uv is not installed.")

    asyncio.run(main())