# TrendCN — GitHub 每日热榜中文站

> ⭐ 每天自动抓取 GitHub Trending，翻译为中文展示  
> 🌐 在线访问：**https://celandine410.github.io/trendcn** (部署后生效)

---

## ✨ 特性

| 特性 | 说明 |
|------|------|
| 🤖 **全自动运行** | GitHub Actions 每天 4 次自动更新，无需人工干预 |
| 🌏 **中文翻译** | 项目描述自动翻译为中文（支持百度翻译 API） |
| 🎨 **精美界面** | GitHub 风格暗色主题，手机电脑自适应 |
| 🏷️ **按语言分类** | Python/JS/Go/Rust 等 17 种语言分类浏览 |
| 🔥 **综合热门榜** | 所有语言合并去重，一眼看全貌 |
| 📊 **多时间维度** | 今日/本周/本月热榜切换 |
| 💰 **完全免费** | 零成本部署，开源免费使用 |

## 🚀 快速开始

### 本地运行

```bash
# 安装依赖
pip install -r requirements.txt

# 运行（默认今日）
python main.py

# 指定时间范围
python main.py --since weekly
python main.py --since monthly

# 使用缓存（避免重复爬取）
python main.py --cache
```

### 启用中文翻译（可选）

1. 注册 [百度翻译开放平台](https://fanyi-api.baidu.com/)（免费版每月 200 万字符）
2. 在项目根目录创建 `.env` 文件或在 GitHub Secrets 中配置：
   ```
   BAIDU_APP_ID=你的AppID
   BAIDU_SECRET_KEY=你的密钥
   ```

## 📁 项目结构

```
trendcn/
├── main.py                 # 入口
├── pyproject.toml          # 项目配置
├── requirements.txt        # 依赖
├── src/
│   ├── config.py           # 配置
│   ├── scraper.py          # GitHub Trending 爬虫
│   ├── translator.py       # 百度翻译模块
│   └── generator.py        # 静态页面生成器
├── docs/                   # 生成的静态页面
├── data/                   # 数据缓存
└── .github/workflows/      # GitHub Actions 自动部署
```

## 🛠️ 技术栈

- **Python** — 数据采集 + 处理
- **httpx + BeautifulSoup** — 网页爬取
- **GitHub Actions** — 定时调度 + 自动部署
- **GitHub Pages** — 免费托管
- **百度翻译 API** — 可选翻译能力

## 💡 变现方式

本项目完全开源免费，如果你觉得有用：  
- ❤️ [爱发电赞助](https://afdian.com/a/celandine410)   
- ⭐ 在 GitHub 上给项目点 Star  
- 📢 分享给你的朋友/同学

## 📄 许可

MIT License

## 🙏 数据来源

[GitHub Trending](https://github.com/trending) — 感谢 GitHub 提供的开放数据
