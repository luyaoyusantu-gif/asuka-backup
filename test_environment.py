#!/usr/bin/env python3
"""
环境测试脚本 - 检查Python环境，测试EVO Map技术实施，准备LiveKit开发
"""

import sys
import subprocess
import importlib.util
import os
from pathlib import Path

print("=" * 60)
print("🧪 环境测试脚本 - EVO Map技术实施验证")
print("=" * 60)

# 基本信息
print(f"\n📋 Python环境信息:")
print(f"  Python版本: {sys.version}")
print(f"  可执行文件: {sys.executable}")
print(f"  工作目录: {os.getcwd()}")
print(f"  平台: {sys.platform}")

# 检查虚拟环境
in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
print(f"  虚拟环境: {'是' if in_venv else '否'}")
if in_venv:
    print(f"  虚拟环境路径: {sys.prefix}")

print("\n🔍 检查EVO Map技术实施文件:")

# 检查实现的文件
impl_files = [
    ("websocket_reconnect.py", "WebSocket全抖动重连算法"),
    ("async_throttle.py", "异步HTTP限流客户端"),
    ("Dockerfile.optimized", "Docker层缓存优化"),
    ("evomap-knowledge.md", "EVO Map技术知识库"),
    ("learning-plan.md", "学习计划"),
    ("livekit_test_plan.md", "LiveKit测试计划"),
]

all_files_exist = True
for filename, description in impl_files:
    filepath = Path(filename)
    exists = filepath.exists()
    status = "✅ 存在" if exists else "❌ 缺失"
    all_files_exist = all_files_exist and exists
    print(f"  {status} {filename} - {description}")

print(f"\n📦 检查Python包依赖:")

# 检查关键包
required_packages = [
    ("asyncio", "内置", True),  # Python 3.4+ 内置
    ("logging", "内置", True),
    ("random", "内置", True),
    ("time", "内置", True),
]

# 第三方包检查
third_party_packages = [
    ("websockets", "WebSocket通信", False),  # websocket_reconnect.py 需要
    ("httpx", "异步HTTP客户端", False),      # async_throttle.py 需要
    ("aiohttp", "aiohttp客户端", False),      # 备用
]

all_packages_ok = True
for package, description, is_builtin in required_packages + third_party_packages:
    try:
        if is_builtin:
            # 内置模块
            importlib.import_module(package)
            status = "✅ 已安装"
        else:
            # 第三方包
            spec = importlib.util.find_spec(package)
            status = "✅ 已安装" if spec else "❌ 未安装"
            if not spec:
                all_packages_ok = False
    except ImportError:
        status = "❌ 导入失败"
        all_packages_ok = False
        if not is_builtin:
            all_packages_ok = False
    
    print(f"  {status} {package} - {description}")

print("\n🚀 LiveKit相关包检查:")

# LiveKit 相关包
livekit_packages = [
    ("livekit", "LiveKit核心SDK", False),
    ("livekit.agents", "LiveKit Agents", False),
    ("livekit.plugins", "LiveKit插件", False),
]

livekit_available = True
for package, description, _ in livekit_packages:
    try:
        spec = importlib.util.find_spec(package.split('.')[0])  # 只检查顶级包
        if spec:
            # 尝试导入看看是否真正可用
            __import__(package.split('.')[0])
            status = "✅ 已安装"
        else:
            status = "❌ 未安装"
            livekit_available = False
    except ImportError:
        status = "❌ 导入失败"
        livekit_available = False
    
    print(f"  {status} {package} - {description}")

print("\n⚡ 系统能力测试:")

# 测试异步功能
async_capable = False
try:
    import asyncio
    # 检查事件循环
    try:
        loop = asyncio.get_event_loop()
        async_capable = True
        print(f"  ✅ 异步支持: 事件循环可用")
    except:
        print(f"  ⚠️  异步支持: 需要创建新事件循环")
        async_capable = True  # 仍然支持，只是需要创建
except ImportError:
    print(f"  ❌ 异步支持: asyncio不可用")

# 测试网络访问能力
network_capable = False
try:
    import socket
    # 简单的socket测试
    socket.create_connection(("8.8.8.8", 53), timeout=2)
    network_capable = True
    print(f"  ✅ 网络访问: 基本连接正常")
except:
    print(f"  ⚠️  网络访问: 测试失败（可能受限制）")

print("\n📊 测试结果总结:")
print("-" * 40)

results = {
    "文件完整性": "✅ 全部存在" if all_files_exist else "⚠️  部分缺失",
    "Python包依赖": "✅ 满足基本需求" if all_packages_ok else "⚠️  需要安装第三方包",
    "LiveKit环境": "✅ 已就绪" if livekit_available else "❌ 需要安装",
    "异步支持": "✅ 可用" if async_capable else "❌ 不可用",
    "网络访问": "✅ 正常" if network_capable else "⚠️  受限",
}

for key, value in results.items():
    print(f"  {key}: {value}")

print("\n🎯 建议操作:")

if not all_packages_ok:
    print("  1. 安装缺失的第三方包:")
    missing = []
    for package, description, is_builtin in third_party_packages:
        if not importlib.util.find_spec(package):
            missing.append(package)
    if missing:
        print(f"     pip install {' '.join(missing)}")

if not livekit_available:
    print("  2. 安装LiveKit SDK:")
    print("     pip install livekit-agents livekit-plugins-openai livekit-plugins-deepgram")

print("  3. 测试EVO Map技术实现:")
print("     - 运行 websocket_reconnect.py 测试")
print("     - 运行 async_throttle.py 测试")
print("     - 验证 Dockerfile.optimized 构建")

print("  4. 准备LiveKit开发:")
print("     - 申请测试API Key")
print("     - 创建最小语音Agent原型")

print("\n💡 环境使用建议:")
print(f"  当前Python: {sys.executable}")
if Path(".venv-nano").exists():
    print(f"  虚拟环境: .venv-nano/ 可用")
    print(f"    激活命令: .venv-nano\\Scripts\\activate (Windows)")
    
print("\n" + "=" * 60)
print("🧪 测试完成 - 准备进入下一阶段")
print("=" * 60)

# 返回总结状态
if all_files_exist and async_capable:
    print("\n🎉 环境基本就绪，可以开始测试EVO Map技术实施")
    sys.exit(0)
else:
    print("\n⚠️  环境需要准备，请先解决上述问题")
    sys.exit(1)