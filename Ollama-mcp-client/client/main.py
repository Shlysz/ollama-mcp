import asyncio

from McpClient import MCPClient

async def main():
    mcp_client = MCPClient()
    await mcp_client.connect_to_server()
    try:
       res= await mcp_client.chat_loop()
       print(res)
    finally:
        await mcp_client.cleanup()





if __name__ == '__main__':
    asyncio.run(main())