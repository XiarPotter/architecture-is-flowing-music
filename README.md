# 建筑是流动的音乐 · Architecture is Flowing Music

> 把"建筑是凝固的音乐"倒过来——让一栋建筑被听见。
> Let a building be _heard_, not just _seen_.

一个建筑生的 vibecoding 实验：把 4 张建筑图（贝聿铭 / 蒙德里安 / 阿那亚 / MAD）转译为 4 段原创配乐（24/22/28/32 秒），并用"水流动 / 金色曲线 / 撕纸拼贴"作为播放态的可视化语言。

A building student's vibecoding experiment: four architectural images (I.M. Pei, Mondrian-style facade, Aranya Chapel, MAD organic canopy) transposed into four original ambient tracks (24/22/28/32 sec), visualized through flowing water, golden signature curves, and torn-paper collage.

---

## 🎧 在线试听 · Live Demo

| 版本 | Version | 风格 · Style | 链接 · Link |
|---|---|---|---|
| v0 | original | 黑白克制 · minimalist B&W | [original.html](./original.html) |
| v1 | collage | 拼贴杂志 · collage magazine | [index.html](./index.html) |
| v2 | editorial | 书页出版物 · editorial booklet | [editorial.html](./editorial.html) |
| **v3** | **poster** | **方形海报 · poster edition（推荐 · recommended）** | [**poster.html**](./poster.html) |

四版页脚互相跳转 · All four versions cross-link in the footer.

---

## 🎼 四段配乐 · Four Tracks

| # | 建筑 · Building | 长度 | 关键词 · Keywords |
|---|---|---|---|
| 01 | 贝聿铭感几何白墙 · Pei-inspired geometric minimal | 24s | 折线 · 秩序 · 镜像 · 留白 |
| 02 | 蒙德里安风格色块网格 · Mondrian urban grid | 22s | 网格 · 色块 · 街头 · 切分 |
| 03 | 阿那亚礼堂清晨 · Aranya dawn chapel | 28s | 尖顶 · 台阶 · 海边 · 孤独 |
| 04 | MAD 有机曲面鸟瞰 · MAD organic canopy | 32s | 伞盖 · 生长 · 放射 · 呼吸 |

---

## ✨ 特色 · Highlights

### v3 poster 版 · Poster Edition
- **1:1 方形海报**：建筑图铺满置底，拼贴诗与大字短语浮于其上
  **Square posters** with full-bleed architecture photos and floating collage poetry
- **每首歌有自己的签名曲线**：前端预解析 wav → 每张海报画一条独一无二的响度曲线
  **Each track has a unique "signature curve"**: pre-decoded from the wav, drawn live as you play
- **48 个关键词全部可点**：点击翻转纸片 → 弹出米黄胶带小卡片，附一句诗意解读
  **All 48 keywords are clickable**: tap to flip and reveal a poetic note
- **上传图片生成音乐**：页面底部上传自己的建筑图 → 分析光影/饱和度/纹理 → 现场合成 24s ambient → 即时变成新海报
  **Upload your own building image** → analyzed for luminance, saturation & texture → synthesized into a 24-sec ambient piece in-browser → immediately becomes the next poster

---

## 🏃 本地运行 · Run Locally

```bash
git clone https://github.com/XiarPotter/architecture-is-flowing-music.git
cd architecture-is-flowing-music
python3 -m http.server 5180
# 浏览器打开 · Open in browser:
# http://localhost:5180/poster.html
```

---

## 🗂 项目结构 · Project Structure

```
vibecoding/
├── poster.html              # v3 · 推荐版本 · featured
├── index.html               # v1 · collage
├── editorial.html           # v2 · editorial
├── original.html            # v0 · original
├── generate_architecture_music.py   # 音乐生成脚本（Python）
├── images/                  # 4 张建筑图
├── output/                  # 4 段 wav
└── VERSIONS.md              # 四版详细档案
```

详细的版本档案见 [VERSIONS.md](./VERSIONS.md)。
For full version archive, see [VERSIONS.md](./VERSIONS.md).

---

## 🛠 技术栈 · Stack

- **前端 · Frontend**: 纯 HTML / CSS / Canvas / Web Audio API（无框架 · no framework）
- **音乐生成 · Music Synthesis**: Python + numpy（离线生成四段 wav）/ OfflineAudioContext（浏览器内合成用户上传图片的音乐）
- **可视化 · Visualization**: `fetch + decodeAudioData` 预解析响度 → Canvas Bezier 曲线绘制

---

## 💡 关于 vibecoding · About vibecoding

> 我一行 CSS 都没写。但我全程在判断、挑剔、塞参考图。
> I didn't write a single line of CSS. But I judged, curated, and fed reference images the whole way.

**AI 负责快，人负责慢**——快的是落地，慢的是审美与取舍。
**AI handles speed, humans handle slowness** — speed in execution, slowness in taste and judgement.

---

## 📄 License

MIT — 随便用、随便改、记得标注来源就好。
Do whatever you want, just leave a link back.

---

Made with ☕ and a lot of reference images by **lunxia (阿屿)** · 2026
