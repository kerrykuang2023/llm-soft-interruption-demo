# 🤖 LLM Agent Soft Interruption Demo

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/Gradio-6.0+-green.svg" alt="Gradio 6.0+">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT">
  <img src="https://img.shields.io/badge/Status-Active-success.svg" alt="Status: Active">
</p>

<p align="center">
  <b>智能对话中的优雅中断：让 LLM 在关键时刻主动寻求确认</b>
</p>

<p align="center">
  <a href="#-demo">🎬 在线演示</a> •
  <a href="#-features">✨ 特性</a> •
  <a href="#-quick-start">🚀 快速开始</a> •
  <a href="#-how-it-works">🔧 工作原理</a> •
  <a href="#-use-cases">💡 应用场景</a>
</p>

---

## 🌟 项目简介

这是一个基于 **Gradio** 构建的交互式演示项目，展示了 LLM Agent 在对话过程中如何优雅地处理**软中断（Soft Interruption）**场景。

当 AI 检测到需要进一步确认的业务细节时，它会主动暂停对话流程，弹出确认对话框请求用户输入，确保生成的方案完全符合业务需求。

> 💡 **核心理念**：AI 不应该假设，而应该确认。在关键业务决策点引入人机协作，让 AI 成为真正的智能助手，而非黑盒。

---

## 🎬 Demo

<img width="1066" height="874" alt="image" src="https://github.com/user-attachments/assets/8603ac2d-ba2f-4733-bc68-b3b4a1cec8ab" />


### 交互流程演示

```
👤 用户: 帮我创建一个电商订单处理系统

🤖 AI: 我来帮您设计电商订单处理系统...
       💭 检测到缺少关键业务信息...

⏸️ [软中断触发] 🛒 订单金额确认
   ├─ 问题：订单金额计算是否需要包含运费？
   ├─ 上下文：影响订单总金额计算逻辑
   └─ 选项：✅包含运费 / ❌不包含 / ⚡满额免运费

👤 用户选择: ⚡ 满额免运费

✅ AI: 已确认！继续对话...

[后续还有 3 个业务确认点...]

🎉 最终生成完整的电商系统方案
```

---

## ✨ Features

### 🎯 智能中断检测
- **上下文感知**：AI 自动识别对话中缺失的关键业务信息
- **精准触发**：在恰当的时机发起确认请求，不打断用户思路
- **渐进式确认**：分阶段收集信息，避免一次性提问过多

### 💬 优雅的交互设计
- **清晰的视觉层次**：标题、问题、上下文、选项层层递进
- **可折叠的上下文说明**：用户可随时查看为什么需要确认
- **智能默认值**：基于常见场景提供合理的默认选项

### 🎨 丰富的场景模拟
本项目模拟了 **电商订单系统** 设计过程中的 4 个典型确认场景：

| 确认点 | 类型 | 业务影响 |
|--------|------|----------|
| 🛒 订单金额确认 | 业务规则 | 影响价格计算和优惠策略 |
| 📊 订单状态流转 | 工作流 | 影响用户体验和库存管理 |
| 📦 库存扣减策略 | 数据一致性 | 影响超卖风险和系统性能 |
| 💰 退款处理规则 | 业务规则 | 影响财务流程和用户信任 |

### 🔧 技术亮点
- **实时状态同步**：使用多线程实现对话流与 UI 的实时更新
- **状态机管理**：清晰管理对话的多种状态（进行中/等待确认/已完成）
- **可扩展架构**：易于添加新的确认场景和业务逻辑

---

## 🚀 Quick Start

### 环境要求

- Python 3.8+
- pip 包管理器

### 安装步骤

1. **克隆仓库**

```bash
git clone https://github.com/kerrykuang2023/llm-soft-interruption-demo.git
cd llm-soft-interruption-demo
```

2. **安装依赖**

```bash
pip install gradio
```

3. **运行演示**

```bash
python agent_meeting_demo.py
```

4. **访问应用**

打开浏览器访问 http://localhost:7860

---

## 🔧 How It Works

### 架构概览

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  Chat History │  │ Status Bar   │  │ Control Panel│  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│  ┌──────────────────────────────────────────────────┐  │
│  │         Soft Interruption Dialog                  │  │
│  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐    │  │
│  │  │ Title  │ │Question│ │Context │ │Options │    │  │
│  │  └────────┘ └────────┘ └────────┘ └────────┘    │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                  Conversation Engine                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Scenario   │  │   State      │  │   Timer      │  │
│  │   Loader     │  │   Manager    │  │   Refresh    │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### 核心流程

1. **场景定义**：在 `LLM_SCENARIOS` 中预定义对话流程和确认点
2. **状态管理**：使用全局状态对象跟踪对话进度和确认结果
3. **线程控制**：后台线程驱动对话流程，主线程保持 UI 响应
4. **定时刷新**：每 0.5 秒刷新 UI，实时反映对话状态变化

### 代码结构

```python
agent_meeting_demo.py
├── LLM_SCENARIOS          # 对话场景定义
├── chat_state            # 全局状态管理
├── conversation_flow()   # 对话流程控制
├── refresh_ui()          # UI 刷新逻辑
└── confirm_answer()      # 确认处理逻辑
```

---

## 💡 Use Cases

### 🛒 电商系统
- 运费计算规则确认
- 库存扣减策略选择
- 退款流程配置
- 促销活动规则设定

### 📊 企业 workflow
- 审批流程节点确认
- 权限规则配置
- 数据验证规则设定
- 异常处理策略选择

### 💰 金融系统
- 费率计算规则确认
- 风控阈值设定
- 合规检查点配置
- 结算周期选择

### 🏥 医疗系统
- 诊断确认机制
- 用药剂量验证
- 禁忌症检查
- 治疗方案选择

---

## 🎨 Customization

### 添加新的确认场景

```python
{
    "role": "assistant",
    "content": "",
    "avatar": "🤖",
    "interrupt": {
        "id": "confirm_custom",
        "type": "business_rule",
        "title": "🎯 你的确认标题",
        "question": "需要确认的问题？",
        "context": "为什么需要确认的详细说明...",
        "options": [
            {"value": "option1", "label": "选项1", "desc": "选项1说明"},
            {"value": "option2", "label": "选项2", "desc": "选项2说明"},
        ],
        "default": "option1"
    }
}
```

### 自定义样式

修改 Gradio Blocks 中的 CSS 参数：

```python
with gr.Blocks(css="""
    .your-custom-class { 
        /* 你的样式 */
    }
""") as demo:
```

---

## 🤝 Contributing

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

---

## 📄 License

本项目基于 MIT 许可证开源 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

## 🙏 Acknowledgments

- [Gradio](https://gradio.app/) - 优秀的 Python Web UI 框架
- [OpenAI](https://openai.com/) - 启发对话式 AI 设计思路
- 所有贡献者和用户 ❤️

---

<p align="center">
  <b>Made with ❤️ by <a href="https://github.com/kerrykuang2023">@kerrykuang2023</a></b>
</p>

<p align="center">
  <a href="https://github.com/kerrykuang2023">GitHub</a> •
  <a href="mailto:your.email@example.com">Email</a>
</p>
