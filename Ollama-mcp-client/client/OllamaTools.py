
"""
the mcp tool format is like
 {'description': 'Get weather forecast for a specific latitude/longitude', 'input_schema': {'additionalProperties': False, 'properties': {'arg0': {'format': 'double', 'type': 'number'}, 'arg1': {'format': 'double', 'type': 'number'}}, 'required': ['arg0', 'arg1'],
  'type': 'object'}, 'name': 'getWeatherForecastByLocation'}
 this func is used to convert the mcp tool format to ollama tool format
"""
class OllamaTools:
    def __init__(self):
        pass

    @staticmethod
    def register_tool(name: str, description: str, inputSchema: dict) -> dict:
        """
        Register a function as a tool.
        """
        properties = inputSchema['properties']
        required = inputSchema['required']
        parameters_type = inputSchema['type']
        tool = {
            'type': 'function',
            'function': {
                'name': name,
                'description': description,
                'parameters': {
                    'type': parameters_type,
                    'properties':properties,
                },
                'required': required
            }
        }
        print(tool)

        return tool

