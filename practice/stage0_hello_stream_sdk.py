"""阶段 0 · 用官方 openai SDK 调 DeepSeek（和零依赖版对照）

用法：
    set DEEPSEEK_API_KEY=sk-xxx
    python stage0_hello_stream_sdk.py "用一句话介绍你自己"

DeepSeek 兼容 OpenAI 协议，所以只需要改 base_url 和 model。
对比 stage0_hello_stream.py：那个手写了 HTTP + SSE 解析，这个交给 SDK。
面试时两种都能讲：SDK 版快，手写版你知道每一层。
"""
import os
import sys

from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY", ""),
    base_url="https://api.deepseek.com",
)


def ask(question: str) -> None:
    stream = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": question}],
        stream=True,
    )
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            print(delta, end="", flush=True)
    print()


if __name__ == "__main__":
    if not os.environ.get("DEEPSEEK_API_KEY"):
        sys.exit("请先设置环境变量 DEEPSEEK_API_KEY")
    ask(" ".join(sys.argv[1:]) or "用一句话介绍你自己")
