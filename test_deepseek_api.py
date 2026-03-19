#!/usr/bin/env python3
"""
测试DeepSeek API连接
"""

import os
import sys
import json
try:
    import httpx
except ImportError:
    print("需要安装httpx: pip install httpx")
    sys.exit(1)

# DeepSeek API密钥
api_key = "sk-960259aedeee4735a8bf7139a1677ad6"
url = "https://api.deepseek.com/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

data = {
    "model": "deepseek-chat",
    "messages": [
        {"role": "user", "content": "Hello, test"}
    ],
    "max_tokens": 10,
    "temperature": 0.1
}

async def test():
    print("测试DeepSeek API连接...")
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(url, headers=headers, json=data)
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("✅ API连接成功!")
                print(f"模型: {result.get('model', 'N/A')}")
                print(f"回复: {result['choices'][0]['message']['content']}")
                return True
            elif response.status_code == 401:
                print("❌ 认证失败: API密钥无效")
                print(f"响应: {response.text[:200]}")
                return False
            elif response.status_code == 429:
                print("⚠️  API限制: 请求过多")
                return False
            else:
                print(f"❌ 请求失败: {response.status_code}")
                print(f"响应: {response.text[:500]}")
                return False
        except Exception as e:
            print(f"❌ 连接异常: {e}")
            return False

if __name__ == "__main__":
    import asyncio
    success = asyncio.run(test())
    sys.exit(0 if success else 1)