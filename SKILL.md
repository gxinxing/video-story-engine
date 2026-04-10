---
name: video-story-engine
description: 基于 Wan 2.7 的 AI 视频故事引擎。一句话输入故事脚本，自动解析分镜、调用万相 2.7 文生视频 API，批量生成多个短片片段。支持赛博朋克/奇幻/悬疑/动漫/自然/科幻六大风格。
icon: 🎬
version: 1.0.0
author: QClaw Agent (Simon)
tags: [视频生成, AI, Wan2.7, 分镜, 短视频, 万相, 故事创作]
created: 2026-04-10
competition: WaytoAGI G1 2.7 Skill Flash Competition
---

# 🎬 AI 视频故事引擎 | Video Story Engine

> WaytoAGI 整活计划第十二期「万相妙思+」快闪赛参赛作品
> 基于阿里云万相 Wan 2.7 API · QClaw Agent 开发

---

## 🎥 Demo 展示

| 片段 | 提示词 | 状态 | 生成时间 |
|------|--------|------|---------|
| 1 | 中文Demo-赛博朋克黑客雨夜 | ✅ | ~60s |
| 2 | Demo-赛博朋克雨夜街头 | ✅ | ~78s |
| 3 | Demo-English Cyberpunk | ✅ | ~114s |
| 4 | Demo-日落海景 | ✅ | ~78s |

> 视频URL为OSS签名临时链接，实际使用时API实时返回有效链接。

---

## 核心能力

**一句话生成完整短片** — 输入故事脚本，自动解析为多个分镜，批量调用 Wan 2.7 文生视频 API，输出多个视频片段。

## 工作流

```
用户输入故事脚本
    ↓
  故事解析（按标点切分，最多8段）
    ↓
  分镜生成（拼接风格预设）
    ↓
  批量调用 Wan 2.7 API（异步任务 + 轮询）
    ↓
  视频 URL 汇总输出
```

## 支持的风格

| 风格 | 代码 | 适用场景 |
|------|------|---------|
| 🌃 赛博朋克 | `cyberpunk` | 都市未来、霓虹夜景 |
| 🏰 奇幻魔法 | `fantasy` | 史诗奇幻、魔法世界 |
| 🕵️ 黑色悬疑 | `noir` | 侦探悬疑、复古电影 |
| 🎨 动漫风格 | `anime` | 治愈日常、动漫风短片 |
| 🌍 自然纪录片 | `nature` | 风光大片、自然纪录 |
| 🚀 科幻太空 | `sci-fi` | 科幻、太空探索 |

## 使用示例

```bash
# 赛博朋克风格故事
python story_engine.py -s "凌晨三点，霓虹闪烁的街头，独自行走的黑客消失在雨幕中" -t cyberpunk

# 奇幻风格（3个分镜）
python story_engine.py -s "巨龙盘旋在古老的城堡上空，骑士举起光明之剑。" -t fantasy -d 5

# 交互模式
python story_engine.py --interactive
```

## 技术亮点

- **异步任务管理**：提交后轮询，状态实时显示
- **智能故事解析**：按中文标点自动分段，适配不同长度输入
- **6种视觉风格预设**：一键切换不同视觉风格
- **SDK 自动安装**：检测依赖缺失时自动 pip install
- **多 Key 来源**：支持环境变量 / 配置文件 / 命令行参数

## 技术规格

- **API**: 阿里云 DashScope 万相 Wan 2.7
- **模型**: `wan2.7-t2v` (Text-to-Video)
- **端点**: `VideoSynthesis.async_call()` + `VideoSynthesis.fetch()`
- **平均生成时间**: 60-120 秒/片段
- **单次最多生成**: 8 个分镜片段
- **提示词语言**: 中文/英文均支持

## 目录结构

```
video-story-engine/
├── SKILL.md           # 本文件（Skill 元数据 + Demo）
├── story_engine.py    # 核心生成引擎
├── run.py             # OpenClaw Skill 入口
├── README.md          # 使用文档
└── demo/
    └── result.json    # Demo 生成结果（含4个视频）
```
