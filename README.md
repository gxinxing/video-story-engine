# 🎬 Video Story Engine

> **一句话生成 AI 短片** — 基于 Wan 2.7 API 的视频故事引擎
>
> WaytoAGI 整活计划第十二期「万相妙思+」快闪赛参赛作品

---

## 🎥 Demo 展示

| # | 视频 | 提示词 | 风格 | 状态 | 耗时 |
|---|------|--------|------|------|------|
| 1 | [▶ 播放](https://dashscope-a717.oss-accelerate.aliyuncs.com/1d/81/20260410/13e23c72/86364518-metadata_d695fd0204e19014.mp4?Expires=1775885160&OSSAccessKeyId=LTAI5tPxpiCM2hjmWrFXrym1&Signature=9%2BEsX%2BlS%2FMdFtDv8KKifj8ecLCE%3D) | 赛博朋克黑客雨夜 | 🌃 cyberpunk | ✅ | ~60s |
| 2 | [▶ 播放](https://dashscope-a717.oss-accelerate.aliyuncs.com/1d/e3/20260410/13e23c72/91086387-metadata_d0aadee712bcb20d.mp4?Expires=1775884614&OSSAccessKeyId=LTAI5tPxpiCM2hjmWrFXrym1&Signature=rbz9SwEshbC6DLuMVre2g43DTJQ%3D) | 赛博朋克雨夜街头 | 🌃 cyberpunk | ✅ | ~78s |
| 3 | [▶ 播放](https://dashscope-a717.oss-accelerate.aliyuncs.com/1d/9b/20260410/13e23c72/61255364-metadata_a9a4df5d68c71a65.mp4?Expires=1775884966&OSSAccessKeyId=LTAI5tPxpiCM2hjmWrFXrym1&Signature=LR1hkZv8VqMDUCjFYZ6UjRl0nbo%3D) | English Cyberpunk | 🌃 cyberpunk | ✅ | ~114s |
| 4 | [▶ 播放](https://dashscope-a717.oss-accelerate.aliyuncs.com/1d/d8/20260410/e8f777a3/96229663-metadata_9fae266a63d9bae2.mp4?Expires=1775884311&OSSAccessKeyId=LTAI5tPxpiCM2hjmWrFXrym1&Signature=vEFpJ0jebGgwDwWhR0XSisavD2k%3D) | 日落海景 | 🌍 nature | ✅ | ~78s |

> ⚠️ 视频为 OSS 签名临时链接，有效期有限，请及时下载保存。

---

## ✨ 核心能力

输入一句话故事脚本，自动：
1. 解析为多个分镜片段
2. 调用阿里云 Wan 2.7 文生视频 API
3. 批量生成视频片段
4. 返回所有视频 URL

```
"凌晨三点，霓虹闪烁的街头，独自行走的黑客消失在雨幕中"
    ↓ 自动解析
[分镜1] 凌晨三点，霓虹闪烁的街头
[分镜2] 独自行走的黑客消失在雨幕中
    ↓ Wan 2.7 生成
✅ 视频1.mp4  ✅ 视频2.mp4
```

---

## 🚀 快速开始

### 安装依赖

```bash
pip install dashscope
```

### 配置 API Key

三种方式任选其一：

```bash
# 方式1: 环境变量（推荐）
export DASHSCOPE_API_KEY=sk-xxxxx

# 方式2: 配置文件
mkdir -p ~/.qclaw/config
echo "sk-xxxxx" > ~/.qclaw/config/wan_api_key

# 方式3: 命令行参数
python story_engine.py -k sk-xxxxx ...
```

> **获取 API Key**: 登录 [阿里云 DashScope](https://dashscope.console.aliyun.com/) → API-KEY 管理 → 创建

### 运行示例

```bash
# 基础用法
python story_engine.py -s "你的故事" -t cyberpunk

# 指定时长
python story_engine.py -s "你的故事" -t fantasy -d 5

# 保存结果
python story_engine.py -s "你的故事" -t sci-fi -o result.json

# 交互模式
python story_engine.py --interactive
```

---

## 🎨 支持的风格

| 风格 | 代码 | 描述 | 适用场景 |
|------|------|------|---------|
| 🌃 赛博朋克 | `cyberpunk` | 霓虹都市、未来感 | 都市未来、黑客、科幻 |
| 🏰 奇幻魔法 | `fantasy` | 史诗奇幻、魔法元素 | 奇幻故事、神话传说 |
| 🕵️ 黑色悬疑 | `noir` | 复古电影、高对比 | 侦探、悬疑、复古 |
| 🎨 动漫风格 | `anime` | 吉卜力风、柔和色彩 | 治愈日常、温馨故事 |
| 🌍 自然纪录 | `nature` | BBC Earth 风格 | 风光、自然、旅行 |
| 🚀 科幻太空 | `sci-fi` | 星际穿越感 | 太空、宇宙、科幻 |

---

## 📖 使用示例

### 赛博朋克风格

```bash
python story_engine.py -s "凌晨三点，霓虹闪烁的街头，独自行走的黑客消失在雨幕中" -t cyberpunk
```

### 奇幻风格

```bash
python story_engine.py -s "巨龙盘旋在古老的城堡上空，骑士举起光明之剑，向黑暗宣战" -t fantasy
```

### 自然纪录风格

```bash
python story_engine.py -s "日出时分，金色的阳光洒在雪山之巅，云海翻涌如潮" -t nature
```

### 科幻太空风格

```bash
python story_engine.py -s "宇航员漂浮在绚丽的星云中，远处是蔚蓝的地球" -t sci-fi
```

---

## ⚙️ 命令行参数

| 参数 | 短参数 | 说明 | 默认值 |
|------|--------|------|--------|
| `--story` | `-s` | 故事脚本（必填） | - |
| `--style` | `-t` | 视觉风格 | `cyberpunk` |
| `--duration` | `-d` | 每片段时长（秒） | `5` |
| `--api-key` | `-k` | API Key | 自动检测 |
| `--output` | `-o` | JSON 结果保存路径 | 不保存 |
| `--interactive` | `-i` | 交互模式 | `False` |

---

## 🔧 技术规格

| 项目 | 值 |
|------|-----|
| **API** | 阿里云 DashScope Wan 2.7 |
| **模型** | `wan2.7-t2v` (Text-to-Video) |
| **SDK** | `dashscope` v1.25.16+ |
| **生成时长** | 60-120 秒/片段 |
| **最大分镜数** | 8 个片段 |
| **支持语言** | 中文 / 英文 |

---

## 📁 目录结构

```
video-story-engine/
├── README.md          # 本文件
├── SKILL.md           # Skill 元数据
├── story_engine.py    # 核心引擎
├── run.py             # OpenClaw 入口
└── demo/
    └── result.json    # Demo 结果
```

---

## 🛠️ 技术亮点

1. **智能故事解析** — 按中文标点自动分段，适配不同长度输入
2. **异步任务管理** — 提交后轮询，状态实时显示
3. **6 种视觉风格** — 一键切换，预设专业级提示词
4. **多 Key 来源** — 环境变量 / 配置文件 / 命令行参数
5. **自动依赖安装** — 检测 dashscope 缺失时自动 pip install

---

## 📝 开发日志

- **2026-04-10** v1.0.0 — 初始版本，完成文生视频核心功能

---

## 📄 License

MIT License

---

## 🔗 相关链接

- **GitHub**: https://github.com/gxinxing/video-story-engine
- **Wan 2.7 文档**: https://help.aliyun.com/zh/model-studio/developer-reference/wanx
- **DashScope 控制台**: https://dashscope.console.aliyun.com/

---

<p align="center">
  Made with 🦞 by <strong>QClaw Agent</strong> for WaytoAGI Competition
</p>
