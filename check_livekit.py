#!/usr/bin/env python3
import sys
import livekit
print("LiveKit模块检查")
print(f"模块路径: {livekit.__file__}")
print(f"模块属性: {dir(livekit)[:10]}...")
# 尝试导入agents
try:
    from livekit import agents
    print("livekit.agents导入成功")
except Exception as e:
    print(f"agents导入失败: {e}")