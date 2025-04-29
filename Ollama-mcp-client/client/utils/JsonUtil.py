import json


def parse_mcp_server_config(file_name):
    """
    Parse the MCP server configuration file.

    Args:
        file_name (str): Path to the MCP server configuration JSON file.

    Returns:
        dict: Parsed server configuration.
    """
    with open(file_name) as f:
        server_config = json.load(f)
        # 解析server_config
        server_dict = server_config['mcpServers']
        return server_dict