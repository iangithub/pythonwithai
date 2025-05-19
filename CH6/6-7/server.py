from mcp.server.fastmcp import FastMCP
import requests

mcp = FastMCP("InventoryServer")


async def inventory(prod: str):
    web_api = "https://koko-demo-api.azurewebsites.net/inventory/"
    response = requests.get(web_api, params={"prod": prod})
    result = response.json()
    print(result)
    return result


@mcp.tool()  
async def get_inventory(query: str):
    """
    get the Inventory by product name.

    Returns:
    dict: The response from the Inventory AI
    """
    response = await inventory(query)
    return response


if __name__ == "__main__":
    mcp.run(transport="stdio")
