# 建筑是流动的音乐 · Architecture is Flowing Music

> 把"建筑是凝固的音乐"倒过来——让一栋建筑被**听见**。
> *Let a building be heard, not just seen.*

一个建筑生的 **vibecoding** 实验：把 4 张建筑图（贝聿铭 / 蒙德里安 / 阿那亚 / MAD）转译为 4 段原创配乐，并用"水流动 × 金色曲线 × 撕纸拼贴"作为播放态的可视化语言。

同一个作品迭代出 **4 个气质完全不同的版本**——你可以从 v0 看到 v3，看见一个 idea 是如何在我和 AI 的来回里被磨出来的。

---

## 🎧 立即体验 · Try It Now

> 推荐 **v3 poster 海报版**，它把这个项目里所有功能都做齐了。

### 🏆 v3 · poster 海报版（演示主版本）

| 入口 | URL |
|---|---|
| 🚀 **GitHub Pages** | [poster.html](https://xiarpotter.github.io/architecture-is-flowing-music/poster.html) |

**设计思路**：每首歌都是一张 1:1 方形海报。建筑图置底铺满，拼贴诗与大字短语浮在蒙层之上，像一张"会动的唱片封面"。

### 其他三版

| 版本 | 设计思路 | 入口 |
|---|---|---|
| v0 · **original 最初版** | 黑白克制、细线水纹——像一份设计研究稿。一切开始的地方。 | [original.html](https://xiarpotter.github.io/architecture-is-flowing-music/original.html) |
| v1 · **collage 拼贴版** | 牛皮纸底 × 撕纸关键词 × 大水纹波形——像一本灵感笔记本，视觉密度最高。 | [index.html](https://xiarpotter.github.io/architecture-is-flowing-music/index.html) |
| v2 · **editorial 书页版** | 暖米白 × 小号 chip × 极简线条波形——像一本听觉小册子，留白最大。 | [editorial.html](https://xiarpotter.github.io/architecture-is-flowing-music/editorial.html) |

**四版页脚互相跳转**，可以在一次浏览里看完一个 idea 的四种表达。

> 💡 如果 GitHub Pages 国内访问慢，使用任何代理工具即可。

---

## 🎼 四段配乐 · Four Tracks

每一张建筑图都对应一段基于它"气质"创作的 ambient 配乐。

| # | 建筑 · Building | 长度 | 声音关键词 · Sound Keywords | 性格 · Character |
|---|---|---|---|---|
| 01 | **贝聿铭感几何白墙**<br>Pei-style Geometric Minimal | 24s | 折线 · 秩序 · 镜像 · 留白 · 屏息 | 低语式几何，不敢大声说话 |
| 02 | **蒙德里安色块网格**<br>Mondrian Urban Grid | 22s | 网格 · 色块 · 街头 · 切分 · 脉冲 | 被切开的城市节拍 |
| 03 | **阿那亚黎明礼堂**<br>Aranya Dawn Chapel | 28s | 尖顶 · 台阶 · 海边 · 孤独 · 浪漫 | 慢波、长尾回响、大范围扩散 |
| 04 | **MAD 有机曲面鸟瞰**<br>MAD Organic Canopy | 32s | 伞盖 · 生长 · 放射 · 呼吸 · 鸟瞰 | 极慢地一推一收，像深呼吸 |

音乐由 `generate_architecture_music.py` 离线生成（Python + numpy 合成，无任何 AI 模型）。

---

## ✨ v3 poster 版的 4 个核心功能

### ① 每首歌有自己的"音乐签名曲线"

不是死板的波形图，而是**每首歌专属的响度曲线**。

- **怎么实现的**：页面加载时 `fetch` 每个 wav → `decodeAudioData` → 取 220 个采样点的响度包络 → 归一化
- **在界面上看到什么**：播放时，一个金色圆点沿着这条曲线从左往右走，走过的部分用金色粗描 + 辉光**保留下来**，未走过的部分用淡色虚线预告。播放完，整首歌的形状就**被画完了**。
- **四张曲线互相对比**：贝聿铭的很平、蒙德里安陡峭、阿那亚舒缓、MAD 几乎是呼吸——**你能一眼看出它们是四首不一样的歌**。

### ② 48 个关键词全部可点

每张海报上的每个贴纸（包括大字短语里每一个单字）都可以点击。

- **交互**：点击 → 纸片翻转 0.55s → 弹出一张**米黄色纸质卡片**（带手撕胶带顶边）
- **内容**：卡片里是这个词对应的一段**诗意化解读**，说明它为什么出现在这首歌里
- **关闭**：点叉号 / 点卡片外空白 / 按 ESC

### ③ 大字短语的"错落拼贴"

"回声中的水"、"被切开的街头节拍"这样的大字短语，每一个字都是**独立的一张小纸片**。

- 4 种底色循环：深米黄 / 黑底白字 / 深蓝底白字 / 米白
- 每张海报指定 2–3 个字额外放大（`xl` / `xxl`），形成视觉重音
- 每个字的基础旋转角度在 ±3° 之间随机，并带 7s 浮动 idle 动画——**静止时也在轻轻呼吸**

### ④ 上传图片 → 现场合成音乐

页面底部有一个拖拽/上传入口，**纯浏览器实现**，不依赖任何后端或 AI API。

- **第一步 · 特征提取**：Canvas 读取图片，分析平均亮度、饱和度、色温、边缘密度
- **第二步 · 参数映射**：
  - 基频 ← 亮度（暗→110Hz，亮→270Hz）
  - 和弦类型 ← 饱和度（浓→小三和弦，淡→纯四/五度）
  - 波形音色 ← 色温（暖→triangle，冷→sine）
  - AM 调幅速率 ← 边缘密度（空旷→0.6Hz，密纹→3Hz）
- **第三步 · 合成**：`OfflineAudioContext` 渲染 24s 音频 → 编码为 wav Blob
- **第四步 · 注入**：立刻变成下方的一张**新海报**，关键词根据图片特征自动生成（如"明亮/浓烈/暖调/密纹"），同样有曲线播放器、可点贴纸

---

## 🎨 建筑 → 音乐 的映射逻辑

每栋建筑有自己的**声场参数**（写在 HTML 的 `data-*` 属性里）：

| 参数 | 含义 | 例 |
|---|---|---|
| `speed` | 水波流动速率 | pei: 0.0007（最慢）· mondrian: 0.00135（最快） |
| `amplitude` | 波幅基线 | mad: 16（最大）· pei: 6（最小） |
| `density` | 水平流线根数 | mondrian: 13（最密）· mad: 8（最疏） |
| `ripple` | 涟漪触发间隔（ms） | mondrian: 1400（最频繁）· mad: 3000（最稀） |

这套参数体系让「**建筑特征 → 音乐参数 → 视觉参数**」可以用同一套规则响应。换一栋楼、改四个数字，整个表现层就跟着换气质。

---

## 🏃 本地运行 · Run Locally

```bash
git clone https://github.com/XiarPotter/architecture-is-flowing-music.git
cd architecture-is-flowing-music
python3 -m http.server 5180
# 然后浏览器打开 · Then open:
#   http://localhost:5180/poster.html     (推荐 · recommended)
#   http://localhost:5180/index.html      (collage)
#   http://localhost:5180/editorial.html  (editorial)
#   http://localhost:5180/original.html   (original)
```

> 💡 注意：`fetch + decodeAudioData` 需要 HTTP 服务器环境，**直接双击 html 文件无法加载音频**。

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
├── VERSIONS.md              # 四版详细档案
└── README.md                # 本文件
```

详细的版本档案见 [VERSIONS.md](./VERSIONS.md)——里面有每一版的完整设计笔记、时间线和气质对照表。

---

## 🛠 技术栈 · Stack

| 层 | 用的东西 | 为什么 |
|---|---|---|
| **前端结构** | 纯 HTML / CSS | 无框架，可直接双击查看源码 |
| **可视化** | Canvas 2D | 画尖刺波形、Bezier 曲线、水滴飞溅 |
| **音频分析** | Web Audio API（`fetch` + `decodeAudioData` + `AnalyserNode`） | 预解析响度包络 + 实时 FFT 能量驱动画面 |
| **图像分析** | Canvas `getImageData` | 从用户上传图提取亮度/饱和度/色温/边缘 |
| **音乐合成（离线四段）** | Python + numpy | `generate_architecture_music.py` 生成 `output/*.wav` |
| **音乐合成（在线生成）** | `OfflineAudioContext` | 浏览器里现场合成用户图片对应的音乐 |
| **部署** | GitHub Pages | 静态站点、免费、HTTPS |

**全程没有调用任何 AI 音乐 / AI 图像 API**，所有逻辑都跑在浏览器或本地脚本里。

---

## 💡 关于 vibecoding · About vibecoding

> 我一行 CSS 都没写。但我全程在判断、挑剔、塞参考图。
> *I didn't write a single line of CSS. But I curated, judged, and fed reference images the whole way.*

**AI 负责快，人负责慢**——快的是落地，慢的是审美与取舍。
**AI handles speed, humans handle slowness** — speed in execution, slowness in taste and judgement.

项目里有 **4 个版本**（加一个上传动态生成的"第 N 版"），不是因为一次做不对，而是因为同一句话（"建筑是流动的音乐"）可以有完全不同的说法。**vibecoding 真正释放的，不是做一个东西的效率，是做很多版的能力。**

---

## 📄 License

MIT — 随便用、随便改，记得标注来源就好。
*Do whatever you want, just leave a link back.*

---

Made with ☕ and a lot of reference images by **lunxia (阿屿)** · 2026
