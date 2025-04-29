import unittest
from client.OllamaTools import OllamaTools


class TestOllamaTools(unittest.TestCase):
    def setUp(self):
        """测试前的初始化"""
        self.tools = OllamaTools()
        self.test_input = {
            'description': 'Get weather forecast for a specific latitude/longitude',
            'input_schema': {
                'additionalProperties': False,
                'properties': {
                    'arg0': {'format': 'double', 'type': 'number'},
                    'arg1': {'format': 'double', 'type': 'number'}
                },
                'required': ['arg0', 'arg1'],
                'type': 'object'
            },
            'name': 'getWeatherForecastByLocation'
        }

    def test_register_tool(self):
        """测试工具注册功能"""
        result = self.tools.register_tool(
            name=self.test_input['name'],
            description=self.test_input['description'],
            inputSchema=self.test_input['input_schema']
        )

        # 验证返回的格式是否正确
        self.assertEqual(result['type'], 'function')
        self.assertEqual(result['function']['name'], 'getWeatherForecastByLocation')
        self.assertEqual(
            result['function']['description'],
            'Get weather forecast for a specific latitude/longitude'
        )

        # 验证参数结构
        self.assertEqual(result['function']['parameters']['type'], 'object')
        self.assertEqual(
            result['function']['parameters']['properties'],
            {
                'arg0': {'format': 'double', 'type': 'number'},
                'arg1': {'format': 'double', 'type': 'number'}
            }
        )
        self.assertEqual(result['function']['required'], ['arg0', 'arg1'])


if __name__ == '__main__':
    unittest.main()