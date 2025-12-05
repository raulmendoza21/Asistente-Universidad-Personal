import asyncio
from fastmcp import Client
from config import MCP_URL


async def _call_mcp_tool_async(tool_name: str, arguments: dict):
    """
    Cliente MCP asincrono: se conecta al servidor y llama a una tool.
    """
    client = Client(MCP_URL)
    async with client:
        result = await client.call_tool(
            name=tool_name,
            arguments=arguments,
        )
    return result


def call_mcp_tool(tool_name: str, **kwargs):
    """
    Wrapper sincrono para poder usarlo desde las herramientas del agente.
    """
    return asyncio.run(_call_mcp_tool_async(tool_name, kwargs))
