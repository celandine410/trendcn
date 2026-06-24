# TrendCN — GitHub 每日热榜中文站

每天自动抓取 [GitHub Trending](https://github.com/trending)，翻译为中文展示。

🌐 **在线访问：** https://celandine410.github.io/trendcn

---

## 页面功能

| 操作 | 说明 |
|------|------|
| **点击语言标签** | 按编程语言筛选（Python / Go / Rust ...） |
| **切换时间范围** | 今日 / 本周 / 本月热榜 |
| **点击仓库名** | 跳转到 GitHub 仓库页面 |

## 本地运行

```bash
# 安装依赖
pip install -r requirements.txt

# 运行（每日热榜）
python main.py

# 本周/本月
python main.py --since weekly
python main.py --since monthly

# 使用缓存（避免重复爬取）
python main.py --cache
```

### 启用中文翻译（可选）

1. 注册 [百度翻译开放平台](https://fanyi-api.baidu.com/)（免费版每月 200 万字符）
2. 在 GitHub 仓库 Settings → Secrets → Actions 添加：
   - `BAIDU_APP_ID`
   - `BAIDU_SECRET_KEY`

## 项目结构

```
trendcn/
├── main.py                 # 入口
├── src/
│   ├── scraper.py          # GitHub Trending 爬虫
│   ├── translator.py       # 百度翻译模块
│   ├── generator.py        # 静态页面生成器
│   └── config.py           # 配置
├── docs/                   # 生成的静态页面
└── .github/workflows/      # GitHub Actions 自动部署
```

## 技术栈

Python + GitHub Actions + GitHub Pages + 百度翻译 API

## 数据来源

[GitHub Trending](https://github.com/trending)
