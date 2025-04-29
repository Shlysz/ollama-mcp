
from contextlib import AsyncExitStack
from typing import Optional

from mcp import ClientSession
from mcp.client.sse import sse_client

import Constants
from client.OllamaAgent import OllamaAgent
from client.utils import JsonUtil


class MCPClient:
    def __init__(self):
        self.session:Optional[ClientSession] = None
        self.exit_stack=AsyncExitStack()
        self.chat_model=OllamaAgent(Constants.LLAMA_MODEL_QWEN)
        self.mcp_server_info=JsonUtil.parse_mcp_server_config(Constants.MCP_SERVER_CONFIG_FILE)

    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()

    async def connect_to_server(self):
        """Connect to an MCP server"""
        mcp_server_name,url=next(iter(self.mcp_server_info.items()))
        base_url=url['url']
        sse_transport = await  self.exit_stack.enter_async_context(sse_client(base_url))
        read, write = sse_transport
        session:ClientSession = await self.exit_stack.enter_async_context(ClientSession(read, write))
        self.session = session
        await self.session.initialize()
        # List available tools
        response = await self.session.list_tools()
        await self.chat_model.register_tools(response)

    async def process_query(self, query: str):
        """Process a query using the MCP server"""
        self.chat_model.messages.append({
            "role": "user",
            "content": query
        })

        final_messages = []

        while True:
            query_response = await self.chat_model.chat()

            # assistant 先说话
            if query_response.message.content:
                content = query_response.message.content
                final_messages.append(content)
                self.chat_model.messages.append({
                    "role": "assistant",
                    "content": content
                })

            # 是否需要调用工具？
            if query_response.message.tool_calls:
                for tool_call in query_response.message.tool_calls:
                    tool_name = tool_call.function.name
                    tool_args = tool_call.function.arguments
                    res = await self.session.call_tool(tool_name, tool_args)
                    tool_result = f"call {tool_name} with args {tool_args}, res: {res}"
                    self.chat_model.messages.append({
                        "role": "tool",
                        "content": tool_result
                    })

                # 工具调用后再进入下一轮模型推理（继续 while）
                continue
            else:
                break  # 没有 tool_call，结束循环，返回

        return final_messages






    async def chat_loop(self):
        """Chat loop to process user input and generate responses"""
        while True:
            try:
                user_prompt = input("How can I help you?\n")
                if user_prompt.lower() in ['quit', 'exit', 'q']:
                    break
                res = await self.process_query(user_prompt)
                print("\nResponse:\n", res)

            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"\nError occurred: {e}")
                break

















