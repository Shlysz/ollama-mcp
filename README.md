# Ollama MCP Client

一个基于Python的客户端实现，用于连接Ollama大语言模型和MCP（Model Context Protocol）服务器，实现模型与外部工具的无缝交互。

## 特性

- 集成Ollama大语言模型（默认使用qwen3:14b）
- 支持SSE（Server-Sent Events）异步通信
- 可扩展的工具调用系统
- 交互式命令行界面
- 简洁的工具格式转换（MCP格式 ⟷ Ollama格式）

## 快速开始

### 环境要求

- Python 3.12+
- Ollama CLI（安装方法请参考 [Ollama官网](https://ollama.com/)）
- java 21+
### 安装

```bash
git clone https://github.com/[username]/ollama-mcp-client
cd ollama-mcp-client
pip install -r requirements.txt
```

### 配置

1. 在 `client/mcp_server_config.json` 配置我的MCP服务器,我的mcp服务器发布在release中,格式如下：
```json
{
  "mcpServers": {
    "server-name": {
      "url": "http://localhost:8080/sse"
    }
  }
}
```
如果你有自己的mcp-server 也可以配置自己的服务器地址。

2. 在 `client/Constants.py` 配置Ollama模型：
```python
LLAMA_MODEL_QWEN = "qwen3:14b"  # 或其他Ollama支持的模型
```

### 运行

```bash
python client/main.py
```

## 项目结构

```
Ollama-MCP-Client
├── client
│   ├── Constants.py
│   ├── McpClient.py
│   ├── OllamaAgent.py
│   ├── OllamaTools.py
│   ├── __init__.py
│   ├── main.py
│   ├── mcp_server_config.json
│   └── utils
│       ├── JsonUtil.py
├── requirements.txt
└── test
    ├── __init__.py
    └── test_ollamaToolsformat.py

```

## 致谢

本项目受到 [mihirrd/ollama-mcp-client](https://github.com/mihirrd/ollama-mcp-client) 的启发,它的项目只支持本地不支持sse，本人的相反，特此感谢。

## 许可证

`MIT License`