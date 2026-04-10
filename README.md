# 🎬 Video Story Engine

> WaytoAGI 整活计划第十二期「万相妙思+」快闪赛参赛作品

## 作品介绍

一句话输入故事脚本，自动解析分镜 → 调用 Wan 2.7 文生视频 API → 批量生成多个短片。

## 快速开始

```bash
# 安装依赖
pip install dashscope

# 运行
python story_engine.py -s "<故事>" -t <风格>
python story_engine.py --interactive  # 交互模式
```

## 风格预览

- 🌃 **cyberpunk** — 赛博朋克霓虹城
- 🏰 **fantasy** — 奇幻魔法世界
- 🕵️ **noir** — 黑色电影悬疑
- 🎨 **anime** — 动漫风格
- 🌍 **nature** — 自然纪录片
- 🚀 **sci-fi** — 科幻太空

## API Key 配置

```bash
# 方式1: 环境变量
export DASHSCOPE_API_KEY=sk-xxxxx

# 方式2: 配置文件
echo "sk-xxxxx" > ~/.qclaw/config/wan_api_key

# 方式3: 命令行参数
python story_engine.py -k sk-xxxxx ...
```
