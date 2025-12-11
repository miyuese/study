# -*- coding: utf-8 -*-
"""
诗歌生成器 - 使用 NewAPI 接口根据用户输入生成诗歌
这是一个简单易用的脚本，适合 Python 小白学习使用
"""

# 导入 requests 库，用于发送 HTTP 请求与 API 服务器通信
# requests 是 Python 中最常用的 HTTP 库，可以轻松发送网络请求
import requests

# 导入 json 库，用于将 Python 字典转换为 JSON 格式，以及解析返回的 JSON 数据
# JSON 是一种常用的数据交换格式，API 通常使用 JSON 格式传输数据
import json

# 定义 NewAPI 的接口地址
# 这是完整的 API 端点 URL，指向 NewAPI 的聊天完成接口
# 注意：URL 必须包含完整的路径 /v1/chat/completions
api_url = "https://newapi.netlib.re/v1/chat/completions"

# 设置您的 API 密钥
# API 密钥用于身份验证，确保您有权限使用该服务
# 请将下面的 "your-api-key-here" 替换为您从 NewAPI 平台获取的实际 API 密钥
api_key = "sk-nKzcJmbO0oP47DSB8QccRp3n7hEKQwzxgfSSuMbCVjmzinF2"

# 设置请求头（headers），这些信息会随请求一起发送给服务器
# headers 告诉服务器关于客户端的一些信息
headers = {
    # Authorization 字段：使用 Bearer 认证方式
    # Bearer 是一种常见的 API 认证方式，格式为 "Bearer 您的API密钥"
    # f"Bearer {api_key}" 是 Python 的字符串格式化，会将 api_key 的值插入到字符串中
    "Authorization": f"Bearer {api_key}",
    
    # Content-Type 字段：告诉服务器我们发送的数据格式是 JSON
    # 这样服务器就知道如何解析我们发送的数据
    "Content-Type": "application/json"
}

# 打印欢迎信息，让用户知道程序的功能
# print() 函数用于在控制台输出文本
# "=" * 50 表示重复 50 次 "=" 符号，用于创建分隔线
print("=" * 50)
print("欢迎使用诗歌生成器！")
print("=" * 50)

# 使用 input() 函数获取用户输入的一句话
# input() 会暂停程序执行，等待用户在控制台输入内容并按下回车键
# 输入的文本会存储在 user_input 变量中
# .strip() 方法用于去除输入内容首尾的空白字符（空格、换行等）
user_input = input("\n请输入一句话，我将为您生成一首诗：").strip()

# 检查用户是否输入了内容
# if not user_input 表示如果 user_input 为空（空字符串）
# 在 Python 中，空字符串被认为是 False，非空字符串被认为是 True
if not user_input:
    # 如果输入为空，打印提示信息并退出程序
    print("\n您没有输入任何内容，程序退出。")
    # exit() 函数用于退出程序
    exit()

# 构建要发送给 API 的请求数据
# 这是一个 Python 字典（dict），类似于其他语言中的对象或映射
# 字典用花括号 {} 表示，包含键值对
data = {
    # model 字段：指定要使用的 AI 模型名称
    # 常见的模型有 "gpt-3.5-turbo"、"gpt-4"、"deepseek-r1" 等
    # 请根据您的 NewAPI 账户中实际可用的模型来修改这个值
    "model": "deepseek-r1-0528",
    
    # messages 字段：包含对话的消息列表
    # 这是一个列表（list），用方括号 [] 表示
    # 列表中的每个元素都是一个字典，代表一条消息
    "messages": [
        # 第一条消息：系统消息，用于设定 AI 的角色和行为
        # role 为 "system" 表示这是系统级别的指令，用于设定 AI 的角色
        {
            "role": "system",
            # content 是具体的指令内容，告诉 AI 要扮演诗人的角色
            # 这里用中文告诉 AI 要创作诗歌
            "content": "你是一个才华横溢的诗人，擅长根据用户输入的一句话创作优美的诗歌。请用中文创作一首诗，要求语言优美、意境深远，并且是格式规范，音韵协调的五言（四句都是五个字）绝句。要求按照以下格式进行回复："
        },
        
        # 第二条消息：用户消息，包含用户刚才输入的内容
        # role 为 "user" 表示这是用户发送的消息
        {
            "role": "user",
            # content 是用户输入的那句话
            # f"..." 是 Python 的 f-string（格式化字符串），可以在字符串中插入变量
            # {user_input} 会被替换为实际用户输入的内容
            "content": f"请根据这句话创作一首诗：{user_input}"
        }
    ],
    
    # max_tokens 字段：限制生成文本的最大长度（以 token 为单位）
    # token 是文本的基本单位，一个汉字大约等于 1-2 个 token
    # 设置为 500 可以生成一首较长的诗
    "max_tokens": 500,
    
    # temperature 字段：控制生成文本的随机性和创造性
    # 取值范围是 0.0 到 2.0
    # 0.0 表示最确定性的输出（每次相同输入产生相同输出）
    # 2.0 表示最随机的输出
    # 0.7 是一个平衡值，既有创造性又不会太随机，适合创作诗歌
    "temperature": 0.7
}

# 使用 try-except 语句块来处理可能出现的错误
# try 块中的代码如果出现错误，会被 except 块捕获，避免程序崩溃
try:
    # 打印提示信息，告诉用户正在处理请求
    print("\n正在为您生成诗歌，请稍候...\n")
    
    # 使用 requests.post() 方法发送 POST 请求到 API 服务器
    # POST 请求用于向服务器发送数据
    # 参数说明：
    #   - api_url: 目标 URL（API 接口地址）
    #   - headers=headers: 指定请求头（包含认证信息）
    #   - json=data: 自动将 data 字典转换为 JSON 格式并发送
    #   - timeout=30: 设置超时时间为 30 秒，如果 30 秒内没有响应就报错
    # 返回的 response 对象包含服务器的响应信息
    response = requests.post(api_url, headers=headers, json=data, timeout=30)
    
    # 检查响应的状态码
    # HTTP 状态码 200 表示请求成功
    # response.status_code 是响应对象的状态码属性
    if response.status_code == 200:
        # 如果请求成功，解析返回的 JSON 数据
        # response.json() 方法将 JSON 格式的响应文本转换为 Python 字典
        # 这样我们就可以方便地访问返回的数据
        response_data = response.json()
        
        # 从响应数据中提取生成的诗歌内容
        # response_data 的结构通常是：
        # {
        #   "choices": [
        #     {
        #       "message": {
        #         "content": "生成的诗歌内容"
        #       }
        #     }
        #   ]
        # }
        # 所以我们需要访问 choices[0].message.content 来获取诗歌
        # [0] 表示列表中的第一个元素（索引从 0 开始）
        poem = response_data['choices'][0]['message']['content']
        
        # 打印分隔线，让输出更美观
        print("=" * 50)
        print("为您生成的诗歌：")
        print("=" * 50)
        
        # 打印生成的诗歌内容
        print(poem)
        
        # 打印结束分隔线
        print("=" * 50)
        
    else:
        # 如果状态码不是 200，说明请求失败
        # 打印错误信息，包括状态码和服务器返回的错误详情
        print(f"❌ 请求失败！")
        print(f"状态码：{response.status_code}")
        print(f"请求的 URL：{api_url}")
        print(f"错误信息：{response.text}")
        
        # 尝试解析错误响应（如果服务器返回的是 JSON 格式的错误信息）
        try:
            # 尝试将响应文本解析为 JSON
            error_data = response.json()
            # 检查错误响应中是否有 message 字段
            if 'error' in error_data and 'message' in error_data['error']:
                # 打印详细的错误信息
                print(f"详细错误：{error_data['error']['message']}")
        except:
            # 如果无法解析为 JSON，就忽略（已经打印了 response.text）
            pass

# 捕获 requests 库可能抛出的异常
# 不同的异常类型需要不同的处理方式

except requests.exceptions.Timeout:
    # 如果请求超时（超过 30 秒没有响应）
    print("❌ 请求超时！请检查网络连接或稍后重试。")

except requests.exceptions.ConnectionError:
    # 如果无法连接到服务器（网络问题或服务器不可用）
    print("❌ 连接失败！请检查网络连接或 API 地址是否正确。")

except requests.exceptions.RequestException as e:
    # 捕获其他所有 requests 相关的异常
    # as e 表示将异常对象赋值给变量 e，这样我们可以访问异常信息
    print(f"❌ 请求发生错误：{str(e)}")

except KeyError as e:
    # 如果响应数据的格式不符合预期，访问字典键时可能出错
    # 例如，如果响应中没有 'choices' 键，访问 response_data['choices'] 就会抛出 KeyError
    print("❌ 解析响应数据时出错，服务器返回的数据格式不正确。")
    print(f"缺少的键：{str(e)}")
    print(f"响应状态码：{response.status_code}")
    print(f"响应内容：{response.text}")

except Exception as e:
    # 捕获所有其他未预料的异常
    # 这是一个兜底的异常处理，确保程序不会因为未知错误而崩溃
    print(f"❌ 发生未知错误：{str(e)}")

# 程序执行完毕，打印结束信息
print("\n感谢使用诗歌生成器！")
