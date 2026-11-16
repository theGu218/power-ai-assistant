"""阶段 0 · 一次直连流式调用（零依赖，只用标准库）

用法：
    set DEEPSEEK_API_KEY=sk-xxxx
    python stage0_hello_stream.py "用一句话介绍你自己"

可用环境变量覆盖：
    DEEPSEEK_BASE_URL  默认 https://api.deepseek.com
    DEEPSEEK_MODEL     默认 deepseek-chat

逐字输出的原理：DeepSeek 返回的是 SSE（Server-Sent Events），
一行一个 "data: {...}"，每个 chunk 里带一小段文字（delta）。
所以不能在循环里 print 整句，要 print(delta, end="", flush=True)。
"""
import json
import os
import sys
import urllib.error
import urllib.request

API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
BASE = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
MODEL = os.environ.get("DEEPSEEK_MODEL", "deepseek-chat")


def ask(question: str) -> None:
    body = json.dumps({
        "model": MODEL,
        "messages": [{"role": "user", "content": question}],
        "stream": True,
    }).encode("utf-8")
    req = urllib.request.Request(
        BASE.rstrip("/") + "/chat/completions",
        data=body,
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + API_KEY},
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            for raw in resp:                      # 按行读，边到边处理
                line = raw.decode("utf-8").strip()
                if not line.startswith("data:"):
                    continue
                data = line[5:].strip()
                if data == "[DONE]":
                    break
                delta = json.loads(data)["choices"][0]["delta"].get("content", "")
                print(delta, end="", flush=True)  # 关键：不换行、立即刷新
        print()                                   # 收尾换行
    except urllib.error.HTTPError as e:
        sys.exit(f"\n[HTTP {e.code}] {e.read().decode('utf-8', 'ignore')[:300]}")


if __name__ == "__main__":
    if not API_KEY:
        sys.exit("请先设置环境变量 DEEPSEEK_API_KEY")
    ask(" ".join(sys.argv[1:]) or "用一句话介绍你自己")
