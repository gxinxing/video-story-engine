#!/usr/bin/env python3
"""
🎬 Video Story Engine - OpenClaw Skill 入口

接收 Agent 的自然语言指令，执行 AI 视频故事生成任务。
由 OpenClaw Skill 系统调用，无需手动运行。

使用方式：
  python run.py --story "<故事>" --style <风格> [--duration 5] [--api-key <密钥>]
  python run.py --interactive

可用风格：cyberpunk | fantasy | noir | anime | nature | sci-fi
"""

import subprocess
import sys
import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()


def main():
    args = sys.argv[1:]

    # 尝试从环境变量获取 API Key
    if not any("--api-key" in a or "-k" in a for a in args):
        key = os.environ.get("DASHSCOPE_API_KEY")
        if key:
            args.extend(["--api-key", key])

    script = SCRIPT_DIR / "story_engine.py"
    cmd = [sys.executable, str(script)] + args

    env = os.environ.copy()
    if "DASHSCOPE_API_KEY" not in env:
        wan_key = os.environ.get("WAN_API_KEY")
        if wan_key:
            env["DASHSCOPE_API_KEY"] = wan_key

    result = subprocess.run(cmd, env=env, cwd=str(SCRIPT_DIR))
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
