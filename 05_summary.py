import os

import requests  # 需要安装requests库

# DeepSeek API的基础URL和模型名称
base_url = "https://api.deepseek.com/chat/completions"
model = "deepseek-chat"

# 读取环境变量中的LLM_API_KEY
api_key = os.environ.get("LLM_API_KEY")
if not api_key:
    raise RuntimeError("请设置环境变量LLM_API_KEY")


# 用于调用DeepSeek API进行文本摘要
def summarize(text):
    # 设置请求头，包含Content-Type和Authorization（使用Bearer Token）
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

    # 构建请求体，包含模型名称和消息内容
    body = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "你是一个摘要助手，把用户给的文章压缩成100字以内，只输出摘要本身，不要任何前言。",
            },
            {"role": "user", "content": text},
        ],
    }

    # 发起POST请求，发送JSON数据到DeepSeek API，设置超时时间为60秒
    response = requests.post(base_url, headers=headers, json=body, timeout=60)

    # 确认请求成功
    if response.status_code != 200:
        # 请求失败，打印状态码和响应正文
        raise RuntimeError(
            f"DeepSeek 请求失败 {response.status_code}: {response.text[:200]}"
        )

    # 将响应正文按JSON解析成Python字典
    data = response.json()

    # 从响应数据中提取模型返回的内容
    response_content = data["choices"][0]["message"]["content"]

    return response_content


# 读取本地文本文件并调用摘要函数
with open("test.txt", "r", encoding="utf-8") as f:
    text = f.read()
print(summarize(text))
