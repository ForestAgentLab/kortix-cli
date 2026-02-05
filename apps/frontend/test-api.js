#!/usr/bin/env node

/**
 * 前端功能测试脚本
 * 测试前端应用是否能正确与后端API通信
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

async function testHealth() {
  console.log('\n🔍 测试 1: 健康检查端点');
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    const data = await response.json();
    console.log('✅ 健康检查成功:', data);
    return true;
  } catch (error) {
    console.error('❌ 健康检查失败:', error.message);
    return false;
  }
}

async function testTools() {
  console.log('\n🔍 测试 2: 获取工具列表');
  try {
    const response = await fetch(`${API_BASE_URL}/v1/tools`);
    const data = await response.json();
    console.log('✅ 工具列表获取成功:', `找到 ${data.tools?.length || 0} 个工具`);
    if (data.tools?.length > 0) {
      console.log('   工具:', data.tools.map(t => t.name).join(', '));
    }
    return true;
  } catch (error) {
    console.error('❌ 获取工具列表失败:', error.message);
    return false;
  }
}

async function testChatReset() {
  console.log('\n🔍 测试 3: 重置对话');
  try {
    const response = await fetch(`${API_BASE_URL}/v1/chat/reset`, {
      method: 'POST',
    });
    const data = await response.json();
    console.log('✅ 重置对话成功:', data);
    return true;
  } catch (error) {
    console.error('❌ 重置对话失败:', error.message);
    return false;
  }
}

async function testHistory() {
  console.log('\n🔍 测试 4: 获取历史记录');
  try {
    const response = await fetch(`${API_BASE_URL}/v1/history?limit=10`);
    const data = await response.json();
    console.log('✅ 历史记录获取成功:', `共 ${data.total} 条消息`);
    return true;
  } catch (error) {
    console.error('❌ 获取历史记录失败:', error.message);
    return false;
  }
}

async function runTests() {
  console.log('=================================');
  console.log('  Kortix 前端功能测试');
  console.log('=================================');
  console.log(`API 地址: ${API_BASE_URL}`);

  const results = [];

  results.push(await testHealth());
  results.push(await testTools());
  results.push(await testChatReset());
  results.push(await testHistory());

  console.log('\n=================================');
  console.log('  测试结果总结');
  console.log('=================================');

  const passed = results.filter(r => r).length;
  const total = results.length;

  console.log(`✅ 通过: ${passed}/${total}`);
  console.log(`❌ 失败: ${total - passed}/${total}`);

  if (passed === total) {
    console.log('\n🎉 所有测试通过！前端应用可以正常使用');
    process.exit(0);
  } else {
    console.log('\n⚠️  部分测试失败，请检查后端服务是否正常运行');
    process.exit(1);
  }
}

runTests().catch(error => {
  console.error('\n❌ 测试执行出错:', error);
  process.exit(1);
});
