import os

import requests  # 需要安装requests库

# 需要安装fastapi库（用于构建Web API的现代Python框架）和uvicorn库（用于运行FastAPI应用）
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# DeepSeek API的基础URL和模型名称
base_url = "https://api.deepseek.com/chat/completions"
model = "deepseek-chat"

# 读取环境变量中的LLM_API_KEY
api_key = os.environ.get("LLM_API_KEY")
if not api_key:
    raise RuntimeError("请设置环境变量LLM_API_KEY")


# 定义一个Pydantic模型，用于验证和解析请求体中的数据
class SummarizeRequest(BaseModel):
    text: str  # 请求体中必须包含一个名为text的字符串字段


# FastAPI应用实例
app = FastAPI()


# 用于调用DeepSeek API进行文本摘要
@app.post("/summarize")
def summarize(request: SummarizeRequest):
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
            {"role": "user", "content": request.text},
        ],
    }

    # 发起POST请求，发送JSON数据到DeepSeek API，设置超时时间为60秒
    response = requests.post(base_url, headers=headers, json=body, timeout=60)

    # 确认请求成功
    if response.status_code != 200:
        # 如果请求失败，抛出HTTP异常，返回状态码和错误详情
        raise HTTPException(
            status_code=502,
            detail=f"上游服务调用失败，状态码 {response.status_code}",
        )
    # 将响应正文按JSON解析成Python字典
    data = response.json()

    # 从响应数据中提取模型返回的内容
    response_content = data["choices"][0]["message"]["content"]

    # 返回摘要结果，作为JSON响应的一部分
    return {"summary": response_content}
