import ollama

from client.OllamaTools import OllamaTools


class OllamaAgent:
    def __init__(self, model_name:str,default_prompt:str="""
    You can call the following tools. Each tool has a name, a description, and an input schema. When the user asks something, choose the most appropriate tool based on its description, and fill in the arguments strictly according to the input schema. Respond only with a JSON object in the format:

{
  "name": "<tool_name>",
  "arguments": { "<arg>": <value>, ... }
}
Do not invent tools or arguments. Use only the provided ones.
 the 'name' is the function name, and the 'arguments' is the function arguments.
 you can not use the tools we do not provide.
    """) -> None:
        self.tools = None
        self.model_name = model_name
        self.messages = [
            {
                "role": "system",
                "content": default_prompt
            }
        ]
        self.default_prompt = default_prompt



    async def register_tools(self, response):
        """
        Register tools with the agent.
        能将mcp的tools 转换为 ollama 的tools类型 方便chat
        :param response:
        """
        print(response.tools)
        self.tools=[
            OllamaTools.register_tool(
                name=tool.name,
                description=tool.description,
                inputSchema=tool.inputSchema
            )
            for tool in response.tools
        ]
        print(self.tools)

    async def chat(self):
        query = ollama.chat(
            model=self.model_name,
            messages=self.messages,
            tools=self.tools,

        )

        return query




async def main():
    agent = OllamaAgent(model_name='qwen3:14b')
    agent.messages=[
        {'role': 'user', 'content': '查一下明天美国加州洛杉矶的天气'}
    ]
    query = await agent.chat()
    print(query)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

