#!/usr/bin/env python3
"""
API 快速测试脚本

验证所有主要端点是否正常工作
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from fastapi.testclient import TestClient

# 导入主应用（api.py 文件）
import api as api_module
app = api_module.app


def test_health():
    """测试健康检查"""
    client = TestClient(app)
    response = client.get("/health")
    print(f"✓ 健康检查: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"  状态: {data['status']}")
        print(f"  工具数: {len(data['tools_enabled'])}")
        return True
    return False


def test_root():
    """测试根路径"""
    client = TestClient(app)
    response = client.get("/")
    print(f"✓ 根路径: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"  名称: {data['name']}")
        print(f"  版本: {data['version']}")
        return True
    return False


def test_tools_list():
    """测试工具列表"""
    client = TestClient(app)
    response = client.get("/v1/tools")
    print(f"✓ 工具列表: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"  工具数: {len(data['tools'])}")
        for tool in data['tools'][:3]:
            print(f"  - {tool['name']}: {len(tool['functions'])} 个函数")
        return True
    return False


def test_chat_completion():
    """测试非流式对话"""
    client = TestClient(app)
    response = client.post(
        "/v1/chat/completion",
        json={"message": "你好，简单介绍一下你自己"}
    )
    print(f"✓ 非流式对话: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"  回复长度: {len(data['content'])} 字符")
        print(f"  预览: {data['content'][:50]}...")
        return True
    return False


def test_history():
    """测试历史接口"""
    client = TestClient(app)
    response = client.get("/v1/history")
    print(f"✓ 对话历史: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"  消息数: {data['total']}")
        return True
    return False


def test_reset():
    """测试重置"""
    client = TestClient(app)
    response = client.post("/v1/chat/reset")
    print(f"✓ 重置对话: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"  成功: {data['success']}")
        return True
    return False


def main():
    """运行所有测试"""
    print("=" * 60)
    print("🧪 FastAPI 后端测试")
    print("=" * 60)
    print()
    
    tests = [
        ("健康检查", test_health),
        ("根路径", test_root),
        ("工具列表", test_tools_list),
        ("对话历史", test_history),
        ("重置对话", test_reset),
        ("非流式对话", test_chat_completion),  # 最后测试，因为会调用 LLM
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
            print()
        except Exception as e:
            print(f"  ❌ 错误: {e}")
            results.append((name, False))
            print()
    
    print("=" * 60)
    print("📊 测试结果")
    print("=" * 60)
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {name}")
    
    print()
    print(f"通过: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 所有测试通过！")
        return 0
    else:
        print(f"\n⚠️  {total - passed} 个测试失败")
        return 1


if __name__ == "__main__":
    sys.exit(main())
