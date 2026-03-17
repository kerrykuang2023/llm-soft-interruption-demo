import gradio as gr
import time
import threading
import json

# 模拟LLM对话场景，包含需要确认的业务细节
LLM_SCENARIOS = [
    {
        "role": "user",
        "content": "帮我创建一个电商订单处理系统",
        "avatar": "👤"
    },
    {
        "role": "assistant",
        "content": "我来帮您设计电商订单处理系统。首先，我需要了解一些业务细节来确保系统符合您的需求。",
        "avatar": "🤖",
        "thinking": "用户需要电商订单系统，但缺少关键业务信息..."
    },
    {
        "role": "assistant",
        "content": "",
        "avatar": "🤖",
        "interrupt": {
            "id": "confirm_1",
            "type": "business_rule",
            "title": "🛒 订单金额确认",
            "question": "检测到业务细节需要确认：订单金额计算是否需要包含运费？",
            "context": "用户提到创建电商订单系统，但未明确说明运费计算规则。这会影响订单总金额的计算逻辑。",
            "options": [
                {"value": "include_shipping", "label": "✅ 包含运费", "desc": "订单金额 = 商品总价 + 运费"},
                {"value": "exclude_shipping", "label": "❌ 不包含运费", "desc": "订单金额仅计算商品总价"},
                {"value": "conditional", "label": "⚡ 满额免运费", "desc": "满一定金额后免运费"}
            ],
            "default": "conditional"
        }
    },
    {
        "role": "assistant",
        "content": "好的，了解了运费规则。接下来我需要确认订单状态流转的细节。",
        "avatar": "🤖",
        "thinking": "已确认运费规则，现在需要确认订单状态机..."
    },
    {
        "role": "assistant",
        "content": "",
        "avatar": "🤖",
        "interrupt": {
            "id": "confirm_2",
            "type": "workflow",
            "title": "📊 订单状态流转",
            "question": "请确认订单取消的时间限制规则：",
            "context": "订单状态从'已支付'到'已发货'之间的取消策略需要明确，这影响库存释放和退款流程。",
            "options": [
                {"value": "anytime", "label": "🔄 发货前随时可取消", "desc": "用户友好，但增加库存管理复杂度"},
                {"value": "30min", "label": "⏱️ 支付后30分钟内", "desc": "防止恶意下单，平衡用户体验"},
                {"value": "no_cancel", "label": "🚫 支付后不可取消", "desc": "简化流程，但用户体验较差"}
            ],
            "default": "30min"
        }
    },
    {
        "role": "assistant",
        "content": "订单状态规则已确认。现在让我了解一下库存相关的业务细节。",
        "avatar": "🤖",
        "thinking": "需要确认库存扣减时机..."
    },
    {
        "role": "assistant",
        "content": "",
        "avatar": "🤖",
        "interrupt": {
            "id": "confirm_3",
            "type": "data_consistency",
            "title": "📦 库存扣减策略",
            "question": "库存扣减应该在哪个时机执行？",
            "context": "库存扣减时机直接影响超卖风险和用户体验。下单时扣减可能导致库存占用，支付时扣减存在超卖风险。",
            "options": [
                {"value": "on_order", "label": "📝 下单时扣减", "desc": "避免超卖，但可能产生无效库存占用"},
                {"value": "on_payment", "label": "💳 支付时扣减", "desc": "减少无效占用，但存在短暂超卖风险"},
                {"value": "hybrid", "label": "🎯 预占+支付扣减", "desc": "下单预占库存，支付时正式扣减"}
            ],
            "default": "hybrid"
        }
    },
    {
        "role": "assistant",
        "content": "库存策略已确认。最后，我需要确认退款处理的相关规则。",
        "avatar": "🤖",
        "thinking": "需要确认退款流程和时效..."
    },
    {
        "role": "assistant",
        "content": "",
        "avatar": "🤖",
        "interrupt": {
            "id": "confirm_4",
            "type": "business_rule",
            "title": "💰 退款处理规则",
            "question": "退款金额计算和到账时效的确认：",
            "context": "退款规则涉及财务流程和用户体验，需要明确是否退运费、优惠券处理以及到账时间。",
            "options": [
                {"value": "full_auto", "label": "⚡ 全额自动退款", "desc": "原路返回，1-3个工作日到账"},
                {"value": "manual_review", "label": "👁️ 人工审核后退款", "desc": "大额订单需审核，3-7个工作日"},
                {"value": "partial_allowed", "label": "🔀 支持部分退款", "desc": "可按商品退款，灵活处理"}
            ],
            "default": "full_auto"
        }
    },
    {
        "role": "assistant",
        "content": "完美！我已经收集了所有关键业务细节。现在为您生成完整的电商订单处理系统方案...",
        "avatar": "🤖",
        "thinking": "所有业务细节已确认，可以生成完整方案"
    },
    {
        "role": "assistant",
        "content": """## 🎯 电商订单处理系统方案

基于您的业务需求，我为您设计了以下系统架构：

### 📋 核心功能模块

**1. 订单管理模块**
- 订单创建与编辑
- 订单状态跟踪（待支付→已支付→待发货→已发货→已完成）
- 订单查询与筛选

**2. 支付处理模块**
- 支持多种支付方式（微信、支付宝、银行卡）
- 支付状态同步与对账
- 支付失败重试机制

**3. 库存管理模块**
- 实时库存查询
- 预占库存机制
- 库存预警与补货提醒

### ⚙️ 已确认的业务规则

| 规则项 | 确认值 | 说明 |
|--------|--------|------|
| 运费计算 | 满额免运费 | 订单金额满99元免运费 |
| 取消限制 | 30分钟内 | 支付后30分钟内可取消 |
| 库存策略 | 预占+扣减 | 下单预占，支付正式扣减 |
| 退款规则 | 全额自动 | 原路返回，1-3个工作日 |

### 🔧 技术实现建议

- 使用分布式事务保证数据一致性
- 采用消息队列处理异步任务
- 实现幂等性防止重复处理

系统方案已生成完毕！如需调整任何业务规则，请告诉我。""",
        "avatar": "🤖"
    }
]

# 全局状态
chat_state = {
    "current_index": 0,
    "is_running": False,
    "waiting_for_confirm": False,
    "chat_history": [],
    "confirm_count": 0,
    "total_confirms": 4,
    "confirmations": {},  # 存储用户的确认结果
    "current_interrupt": None
}

state_lock = threading.Lock()

def get_status_text():
    """获取当前状态文本"""
    if chat_state["waiting_for_confirm"]:
        return f"⏸️ 等待业务确认... ({chat_state['confirm_count']}/{chat_state['total_confirms']})"
    elif chat_state["is_running"]:
        return f"🤔 AI思考中... ({chat_state['confirm_count']}/{chat_state['total_confirms']} 已确认)"
    else:
        return "💬 对话未开始"

def format_chat_history():
    """格式化聊天记录"""
    messages = []
    for item in chat_state["chat_history"]:
        if item["type"] == "message":
            avatar = item.get("avatar", "🤖")
            role_label = "用户" if item.get("role") == "user" else "AI助手"
            messages.append(f"{avatar} **{role_label}**: {item['content']}")
        elif item["type"] == "thinking":
            messages.append(f"> 💭 *{item['content']}*")
        elif item["type"] == "interrupt":
            messages.append(f"\n> 🔴 **业务确认请求**: {item['title']}\n")
        elif item["type"] == "confirm":
            messages.append(f"> ✅ **已确认**: {item['answer']}\n")
    return "\n\n".join(messages)

def start_conversation():
    """开始对话"""
    with state_lock:
        if chat_state["is_running"]:
            return gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update()
        
        chat_state["current_index"] = 0
        chat_state["is_running"] = True
        chat_state["waiting_for_confirm"] = False
        chat_state["chat_history"] = []
        chat_state["confirm_count"] = 0
        chat_state["confirmations"] = {}
        chat_state["current_interrupt"] = None
    
    # 开始对话流程
    threading.Thread(target=conversation_flow, daemon=True).start()
    
    return (
        gr.update(value="对话开始..."),
        gr.update(value=get_status_text()),
        gr.update(visible=False),
        gr.update(visible=False),
        gr.update(visible=False),
        gr.update(visible=False),
        gr.update(visible=False),
        gr.update(visible=False),
        gr.update(interactive=False)
    )

def conversation_flow():
    """对话流程控制"""
    global chat_state
    
    for i, scenario in enumerate(LLM_SCENARIOS):
        with state_lock:
            if not chat_state["is_running"]:
                break
            chat_state["current_index"] = i
        
        # 添加消息到历史
        time.sleep(0.3)
        
        if scenario.get("thinking"):
            with state_lock:
                chat_state["chat_history"].append({
                    "type": "thinking",
                    "content": scenario["thinking"]
                })
            time.sleep(0.5)
        
        # 检查是否需要中断确认
        if scenario.get("interrupt"):
            interrupt_data = scenario["interrupt"]
            with state_lock:
                chat_state["waiting_for_confirm"] = True
                chat_state["current_interrupt"] = interrupt_data
                chat_state["chat_history"].append({
                    "type": "interrupt",
                    "title": interrupt_data["title"],
                    "question": interrupt_data["question"]
                })
            
            # 等待用户确认
            while True:
                with state_lock:
                    if not chat_state["waiting_for_confirm"]:
                        break
                    if not chat_state["is_running"]:
                        return
                time.sleep(0.1)
        else:
            # 普通消息
            with state_lock:
                chat_state["chat_history"].append({
                    "type": "message",
                    "role": scenario["role"],
                    "content": scenario["content"],
                    "avatar": scenario.get("avatar", "🤖")
                })
        
        time.sleep(0.8)
    
    with state_lock:
        chat_state["is_running"] = False

def confirm_answer(answer):
    """处理用户确认"""
    with state_lock:
        if not chat_state["waiting_for_confirm"]:
            return gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update()
        
        interrupt = chat_state["current_interrupt"]
        selected_option = None
        for opt in interrupt["options"]:
            if opt["value"] == answer:
                selected_option = opt
                break
        
        chat_state["chat_history"].append({
            "type": "confirm",
            "answer": selected_option["label"] if selected_option else answer
        })
        chat_state["confirmations"][interrupt["id"]] = {
            "type": interrupt["type"],
            "answer": answer,
            "label": selected_option["label"] if selected_option else answer
        }
        chat_state["waiting_for_confirm"] = False
        chat_state["confirm_count"] += 1
        chat_state["current_interrupt"] = None
    
    return (
        gr.update(value=format_chat_history()),
        gr.update(value=get_status_text()),
        gr.update(visible=False),
        gr.update(visible=False),
        gr.update(visible=False),
        gr.update(visible=False),
        gr.update(visible=False),
        gr.update(visible=False),
        gr.update(interactive=False)
    )

def refresh_ui():
    """刷新UI状态"""
    with state_lock:
        chat_text = format_chat_history()
        status = get_status_text()
        
        # 检查是否需要显示确认对话框
        if chat_state["waiting_for_confirm"] and chat_state["current_interrupt"]:
            interrupt = chat_state["current_interrupt"]
            return (
                gr.update(value=chat_text),
                gr.update(value=status),
                gr.update(value=f"### {interrupt['title']}"),
                gr.update(value=interrupt["question"]),
                gr.update(value=interrupt["context"]),
                gr.update(
                    choices=[(opt["label"], opt["value"]) for opt in interrupt["options"]],
                    value=interrupt["default"],
                    visible=True
                ),
                gr.update(visible=True),
                gr.update(visible=True),
                gr.update(interactive=False)
            )
        else:
            is_completed = chat_state["confirm_count"] >= chat_state["total_confirms"]
            return (
                gr.update(value=chat_text),
                gr.update(value=status),
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(interactive=is_completed or not chat_state["is_running"])
            )

def stop_conversation():
    """停止对话"""
    with state_lock:
        chat_state["is_running"] = False
        chat_state["waiting_for_confirm"] = False
    
    return (
        gr.update(value="对话已停止"),
        gr.update(value=get_status_text()),
        gr.update(visible=False),
        gr.update(visible=False),
        gr.update(visible=False),
        gr.update(visible=False),
        gr.update(visible=False),
        gr.update(visible=False),
        gr.update(interactive=True)
    )

def reset_conversation():
    """重置对话"""
    with state_lock:
        chat_state["current_index"] = 0
        chat_state["is_running"] = False
        chat_state["waiting_for_confirm"] = False
        chat_state["chat_history"] = []
        chat_state["confirm_count"] = 0
        chat_state["confirmations"] = {}
        chat_state["current_interrupt"] = None
    
    return (
        gr.update(value="点击开始按钮启动LLM对话模拟"),
        gr.update(value=get_status_text()),
        gr.update(visible=False),
        gr.update(visible=False),
        gr.update(visible=False),
        gr.update(visible=False),
        gr.update(visible=False),
        gr.update(visible=False),
        gr.update(interactive=True)
    )

# 创建Gradio界面
with gr.Blocks(title="LLM Agent 软中断确认演示") as demo:
    
    gr.Markdown("""
    # 🤖 LLM Agent 软中断确认演示
    
    这个演示模拟了LLM在对话过程中，当检测到需要进一步确认的业务细节时，自动触发软中断请求用户确认的场景。
    
    **典型应用场景：**
    - 🛒 电商系统：运费计算、库存策略、退款规则
    - 📊 业务流程：审批流、状态机、权限规则  
    - 💰 金融系统：费率计算、风控规则、合规检查
    - 🏥 医疗系统：诊断确认、用药剂量、禁忌检查
    """)
    
    with gr.Row():
        with gr.Column(scale=2):
            # 状态栏
            status_text = gr.Textbox(
                value=get_status_text(),
                label="当前状态",
                interactive=False
            )
            
            # 聊天历史
            chat_display = gr.Markdown(
                value="点击开始按钮启动LLM对话模拟",
                label="对话记录"
            )
        
        with gr.Column(scale=1):
            # 控制按钮
            gr.Markdown("### 控制面板")
            start_btn = gr.Button("▶️ 开始对话", variant="primary", size="lg")
            stop_btn = gr.Button("⏹️ 停止", variant="stop", size="lg")
            reset_btn = gr.Button("🔄 重置", variant="secondary", size="lg")
            
            gr.Markdown("---")
            gr.Markdown("### 统计信息")
            stats = gr.Markdown(f"""
            - 待确认项: {chat_state['total_confirms']}
            - 已确认: {chat_state['confirm_count']}
            - 剩余: {chat_state['total_confirms'] - chat_state['confirm_count']}
            """)
    
    # 软中断确认对话框（初始隐藏）
    with gr.Row(visible=False) as confirm_row:
        with gr.Column():
            # 确认标题
            confirm_title = gr.Markdown()
            
            # 问题描述
            confirm_question = gr.Markdown()
            
            # 上下文说明
            with gr.Accordion("📋 为什么需要确认？", open=True):
                confirm_context = gr.Markdown()
            
            # 选项选择
            confirm_radio = gr.Radio(
                choices=[],
                label="请选择业务规则",
                interactive=True
            )
            
            # 确认按钮
            confirm_btn = gr.Button("✅ 确认选择", variant="primary", size="lg")
    
    # 使用定时器自动刷新UI
    timer = gr.Timer(value=0.5, active=True)
    timer.tick(
        fn=refresh_ui,
        outputs=[chat_display, status_text, confirm_title, confirm_question, confirm_context, 
                 confirm_radio, confirm_btn, confirm_row, start_btn]
    )
    
    # 事件绑定
    start_btn.click(
        fn=start_conversation,
        outputs=[chat_display, status_text, confirm_title, confirm_question, confirm_context,
                 confirm_radio, confirm_btn, confirm_row, start_btn]
    )
    
    stop_btn.click(
        fn=stop_conversation,
        outputs=[chat_display, status_text, confirm_title, confirm_question, confirm_context,
                 confirm_radio, confirm_btn, confirm_row, start_btn]
    )
    
    reset_btn.click(
        fn=reset_conversation,
        outputs=[chat_display, status_text, confirm_title, confirm_question, confirm_context,
                 confirm_radio, confirm_btn, confirm_row, start_btn]
    )
    
    confirm_btn.click(
        fn=confirm_answer,
        inputs=[confirm_radio],
        outputs=[chat_display, status_text, confirm_title, confirm_question, confirm_context,
                 confirm_radio, confirm_btn, confirm_row, start_btn]
    )

if __name__ == "__main__":
    demo.launch(share=False, server_name="0.0.0.0", server_port=7860)
