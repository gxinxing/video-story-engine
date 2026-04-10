#!/usr/bin/env python3
"""
Video Story Engine - Wan 2.7 AI Video Story Generator
一句话输入故事脚本，自动解析分镜、调用 Wan 2.7 文生视频 API，批量生成多个短片片段。
用法: python story_engine.py --story "<故事>" --style <风格> [--duration 5]
风格: cyberpunk | fantasy | noir | anime | nature | sci-fi
依赖: pip install dashscope
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

try:
    import dashscope
    dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'
    from dashscope.aigc.video_synthesis import VideoSynthesis
    HAS_DASHSCOPE = True
except ImportError:
    print("Installing dashscope...")
    import subprocess, sys
    r = subprocess.run([sys.executable, "-m", "pip", "install", "dashscope",
                        "-i", "https://pypi.tuna.tsinghua.edu.cn/simple/", "--quiet"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print(f"Install failed: {r.stderr}")
        sys.exit(1)
    import dashscope
    dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'
    from dashscope.aigc.video_synthesis import VideoSynthesis
    HAS_DASHSCOPE = True

STYLE_PRESETS = {
    "cyberpunk": {
        "name": "赛博朋克霓虹城",
        "default_prompt": (
            "cinematic cyberpunk city at night, neon lights everywhere, "
            "rain on streets, futuristic architecture, holographic ads, "
            "high contrast, dramatic lighting, blade runner atmosphere"
        ),
    },
    "fantasy": {
        "name": "奇幻魔法世界",
        "default_prompt": (
            "fantasy magical kingdom, ancient castle on floating islands, "
            "glowing magic particles, epic scale, golden hour light, "
            "mystical atmosphere, breathtaking scenery, cinematic"
        ),
    },
    "noir": {
        "name": "黑色电影悬疑",
        "default_prompt": (
            "film noir detective scene, moody shadows, "
            "rain-soaked streets, vintage 1940s aesthetic, "
            "high contrast black and white with color accents, dramatic"
        ),
    },
    "anime": {
        "name": "动漫风格",
        "default_prompt": (
            "anime style scene, Studio Ghibli inspired, "
            "beautiful countryside, soft pastel colors, "
            "peaceful mood, detailed animation style"
        ),
    },
    "nature": {
        "name": "自然纪录片",
        "default_prompt": (
            "epic nature documentary shot, vast mountain landscape, "
            "golden sunrise, wildlife, aerial drone view, "
            "BBC Earth quality cinematography"
        ),
    },
    "sci-fi": {
        "name": "科幻太空",
        "default_prompt": (
            "sci-fi space scene, astronaut floating in nebula, "
            "distant planets, cosmic dust, volumetric lighting, "
            "interstellar movie aesthetic, 8K quality"
        ),
    },
}

MODEL_T2V = "wan2.7-t2v"


def get_api_key(api_key=None):
    if api_key:
        return api_key
    key = os.environ.get("DASHSCOPE_API_KEY")
    if key:
        return key
    cfg = Path.home() / ".qclaw" / "config" / "wan_api_key"
    if cfg.exists():
        return cfg.read_text().strip()
    return input("\n请输入 DASHSCOPE_API_KEY: ").strip()


def generate_video(api_key, prompt, duration=5, max_wait=300):
    print(f"\n  正在生成... 提示词: {prompt[:80]}{'...' if len(prompt) > 80 else ''}")
    dashscope.api_key = api_key

    resp = VideoSynthesis.async_call(model=MODEL_T2V, prompt=prompt, duration=duration)
    if resp.status_code != 200:
        raise RuntimeError(f"提交失败 [{resp.code}]: {resp.message}")

    task_id = resp.output["task_id"]
    print(f"  任务ID: {task_id}")

    start = time.time()
    while time.time() - start < max_wait:
        resp = VideoSynthesis.fetch(task=task_id)
        output = resp.output
        status = output.get("task_status", "UNKNOWN")
        elapsed = int(time.time() - start)

        if status == "SUCCEEDED":
            video_url = output.get("video_url", "")
            print(f"\n  [OK] 生成完成! 耗时 {elapsed}s")
            return video_url
        elif status in ("FAILED", "CANCELED"):
            raise RuntimeError(f"任务失败: {output.get('code')} - {output.get('message')}")
        else:
            print(f"\r  [{elapsed}s] 状态: {status}   ", end="", flush=True)

        time.sleep(5)

    raise TimeoutError(f"等待超时(>{max_wait}s)")


def parse_story(story, style):
    # 按中文标点分段
    seps = ["\u3002", "\uff1b", "\uff0c", "\n"]
    for sep in seps:
        if sep in story:
            segments = [s.strip() for s in story.split(sep) if s.strip()]
            break
    else:
        segments = [story[i:i+120].strip() for i in range(0, len(story), 120)]

    segments = segments[:8]
    preset = STYLE_PRESETS.get(style, STYLE_PRESETS["cyberpunk"])

    shots = []
    for i, seg in enumerate(segments):
        shot_prompt = (
            f"{seg.strip()}. "
            f"{preset['default_prompt']}, "
            f"cinematic shot {i+1} of {len(segments)}, movie scene"
        )
        shots.append(shot_prompt)
    return shots


def generate_story_video(api_key, story, style, duration=5):
    preset = STYLE_PRESETS.get(style, STYLE_PRESETS["cyberpunk"])
    print(f"\n[Video Story Engine]")
    print(f"  风格: {preset['name']} ({style})")
    print(f"  时长: {duration}s/片段")
    print("-" * 55)

    shots = parse_story(story, style)
    print(f"检测到 {len(shots)} 个分镜\n")

    results = []
    for i, shot_prompt in enumerate(shots):
        print(f"[{i+1}/{len(shots)}] 分镜 {i+1}")
        try:
            video_url = generate_video(api_key, shot_prompt, duration)
            results.append({"shot": i+1, "prompt": shot_prompt, "video_url": video_url, "status": "success"})
        except Exception as e:
            print(f"  [FAIL] {e}")
            results.append({"shot": i+1, "prompt": shot_prompt, "video_url": None, "status": "failed", "error": str(e)})

    success = sum(1 for r in results if r["status"] == "success")
    print(f"\n{'='*55}")
    print(f"[DONE] 成功: {success}/{len(shots)} 个分镜\n")
    for r in results:
        icon = "[OK]" if r["status"] == "success" else "[FAIL]"
        url = r.get("video_url") or r.get("error") or "N/A"
        print(f"  {icon} 分镜{r['shot']}: {url[:80]}")
    print("\n  提示: 视频链接有效期有限，请及时下载保存!")

    return {
        "style": style,
        "style_name": preset["name"],
        "total_shots": len(shots),
        "success_count": success,
        "shots": results,
    }


def main():
    parser = argparse.ArgumentParser(description="[Video Story Engine] Wan 2.7 AI 视频故事引擎")
    parser.add_argument("--story", "-s", required=True, help="故事脚本")
    parser.add_argument("--style", "-t", default="cyberpunk",
                        choices=list(STYLE_PRESETS.keys()), help="视觉风格")
    parser.add_argument("--duration", "-d", type=int, default=5, help="每片段时长(秒)")
    parser.add_argument("--api-key", "-k", default=None, help="DASHSCOPE_API_KEY")
    parser.add_argument("--interactive", "-i", action="store_true", help="交互模式")
    parser.add_argument("--output", "-o", default=None, help="JSON结果保存路径")

    args = parser.parse_args()
    api_key = get_api_key(args.api_key)

    if args.interactive:
        story = input("故事脚本: ").strip()
        style = input(f"风格({', '.join(STYLE_PRESETS.keys())}, 默认cyberpunk): ").strip() or "cyberpunk"
        duration = int(input("时长(秒, 默认5): ").strip() or "5")
    else:
        story, style, duration = args.story, args.style, args.duration

    result = generate_story_video(api_key, story, style, duration)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\n结果已保存: {args.output}")


if __name__ == "__main__":
    main()
