import streamlit as st
import requests
import json

# ==========================================
# 1. 页面基础设置
# ==========================================
st.set_page_config(
    page_title="AI 灵感诗人",
    page_icon="🤖",
    layout="centered"
)

# 标题和简介
st.title("🤖 AI 灵感诗人")
st.markdown("输入一个词或一句话，AI 将为你通过 **DeepSeek** 模型创作诗歌。")

# ==========================================
# 2. 侧边栏配置 (让你的产品看起来更高级)
# ==========================================
with st.sidebar:
    st.header("🎨 创作设置")
    
    # 让用户选择诗歌风格 (这是原来脚本没有的功能！)
    style_option = st.selectbox(
        "选择诗歌风格",
        ["五言绝句 (经典)", "七言律诗 (工整)", "现代诗 (自由)", "幽默打油诗 (有趣)"]
    )
    
    # 调整创意程度 (对应 temperature)
    creativity = st.slider("创意程度 (Temperature)", 0.0, 1.5, 0.7, 0.1)
    
    st.info("💡 提示：创意程度越高，AI 写得越天马行空。")

# ==========================================
# 3. 核心逻辑区域
# ==========================================

# API 配置
API_URL = "https://ai.dik3.cn/v1/chat/completions"
# 这里直接使用了你提供的 Key
API_KEY = "sk-DWST56CwGw29M1vOglY7DREFyA9yZB6FfStuPvzC5f0MxVDf" 

# 获取用户输入
user_input = st.text_input("请输入灵感关键词：", placeholder="例如：雨后的彩虹，或者想念家乡")

# 定义一个生成函数
def generate_poem():
    if not user_input:
        st.warning("⚠️ 请先输入一点灵感关键词！")
        return

    # 根据侧边栏的选择，动态调整 System Prompt
    system_prompt = f"你是一个才华横溢的诗人。请根据用户输入，创作一首【{style_option}】。要求意境深远，格式规范。"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "deepseek-v3.2",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"请以'{user_input}'为题或意象，写一首诗。"}
        ],
        "temperature": creativity
    }

    # 显示加载转圈圈
    with st.spinner('AI 正在推敲韵脚...'):
        try:
            response = requests.post(API_URL, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                # 成功展示
                st.success("✨ 创作完成！")
                st.markdown("---") # 分割线
                st.markdown(f"### 📜 {user_input}") # 显示标题
                st.markdown(content) # 显示诗歌
            else:
                st.error(f"❌ 请求失败，状态码：{response.status_code}")
                st.text(response.text)
                
        except Exception as e:
            st.error(f"❌ 发生错误：{str(e)}")

# ==========================================
# 4. 按钮触发
# ==========================================
if st.button("开始创作", type="primary"):
    generate_poem()